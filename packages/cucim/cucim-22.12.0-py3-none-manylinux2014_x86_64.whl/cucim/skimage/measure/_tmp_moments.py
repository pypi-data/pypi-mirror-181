import cupy as cp

from cucim.skimage import measure

d = cp.cuda.Device()


def _get_moments_norm_operation(ndim, order, unit_scale=True):
    """Full normalization computation kernel for 2D or 3D cases.

    Variants with or without scaling are provided.
    """
    operation = f"""
        double mu0 = static_cast<double>(mu[0]);
        double ndim = {ndim};
        int power_sum;
        int n_rows = order + 1;
    """
    if unit_scale:
        operation += f"""
        double mu0_pows[{order + 1}];
        for (int ord=0; ord <= order; ord++)
        {{
           mu0_pows[ord] = pow(mu0, static_cast<double>(ord) / ndim + 1);
        }}
        """
    else:
        operation += f"""
        double s_pow, denom;
        double s_pows[{order + 1}], mu0_pows[{order + 1}];
        for (int ord=0; ord <= order; ord++)
        {{
           s_pows[ord] = pow(scale, static_cast<double>(ord));
           mu0_pows[ord] = pow(mu0, static_cast<double>(ord) / ndim + 1);
        }}
        """
    if ndim == 2:
        operation += """
        #pragma unroll
        for (int x = 0; x <= order; x++) {
            #pragma unroll
            for (int y = 0; y <= order; y++) {
                power_sum = x + y;
                if ((power_sum > order) || (power_sum < 2))
                {
                    continue;
                }
        """
        if unit_scale:
            operation += """
                nu[y + x*n_rows] = mu[y + x*n_rows] / mu0_pows[power_sum];"""
        else:
            operation += """
                s_pow = s_pows[power_sum];
                denom = mu0_pows[power_sum];
                nu[y + x*n_rows] = (mu[y + x*n_rows] / s_pow) / denom;"""
    elif ndim == 3:
        operation += """
        for (int x = 0; x <= order; x++) {
            for (int y = 0; y <= order; y++) {
                for (int z = 0; z <= order; z++) {
                    power_sum = x + y + z;
                    if ((power_sum > order) || (power_sum < 2))
                    {
                        continue;
                    }
        """
        if unit_scale:
            operation += """
                    nu[z + n_rows*(y + x*n_rows)] = mu[z + n_rows*(y + x*n_rows)] / mu0_pows[power_sum];
            """  # noqa
        else:
            operation += """
                    s_pow = s_pows[power_sum];
                    denom = mu0_pows[power_sum];
                    nu[z + n_rows*(y + x*n_rows)] = (mu[z + n_rows*(y + x*n_rows)] / s_pow) / denom;
            """  # noqa
    else:
        raise ValueError("custom kernel only implemented for 2D and 3D cases")
    operation += "\n" + "}" * ndim
    return operation


@cp.memoize()
def _get_normalize_kernel(ndim, order, unit_scale=True):
    return cp.ElementwiseKernel(
        'raw F mu, int32 order, float64 scale',
        'raw F nu',
        operation=_get_normalize_operation(ndim, order, unit_scale),
        name=f"moments_normmalize_2d_kernel"
    )


@cp.fuse()
def _get_nu(mu, power_sum, mu0, ndim):
    """fused moment normalization kernel for general nD case"""
    return mu / (mu0 ** (power_sum / ndim + 1))


@cp.fuse()
def _get_nu_scaled(mu, scale, power_sum, mu0, ndim):
    """fused (and scaled) moment normalization kernel for general nD case"""
    return ((mu / scale ** power_sum)
            / (mu0 ** (power_sum / ndim + 1)))


def moments_normalized(mu, order=3, spacing=None):
    """Calculate all normalized central image moments up to a certain order.

    Note that normalized central moments are translation and scale invariant
    but not rotation invariant.

    Parameters
    ----------
    mu : (M,[ ...,] M) array
        Central image moments, where M must be greater than or equal
        to ``order``.
    order : int, optional
        Maximum order of moments. Default is 3.

    Returns
    -------
    nu : (``order + 1``,[ ...,] ``order + 1``) array
        Normalized central image moments.

    References
    ----------
    .. [1] Wilhelm Burger, Mark Burge. Principles of Digital Image Processing:
           Core Algorithms. Springer-Verlag, London, 2009.
    .. [2] B. Jähne. Digital Image Processing. Springer-Verlag,
           Berlin-Heidelberg, 6. edition, 2005.
    .. [3] T. H. Reiss. Recognizing Planar Objects Using Invariant Image
           Features, from Lecture notes in computer science, p. 676. Springer,
           Berlin, 1993.
    .. [4] https://en.wikipedia.org/wiki/Image_moment

    Examples
    --------
    >>> import cupy as cp
    >>> from cucim.skimage.measure import (moments, moments_central,
    ...                                      moments_normalized)
    >>> image = cp.zeros((20, 20), dtype=cp.float64)
    >>> image[13:17, 13:17] = 1
    >>> m = moments(image)
    >>> centroid = (m[0, 1] / m[0, 0], m[1, 0] / m[0, 0])
    >>> mu = moments_central(image, centroid)
    >>> moments_normalized(mu)
    array([[       nan,        nan, 0.078125  , 0.        ],
           [       nan, 0.        , 0.        , 0.        ],
           [0.078125  , 0.        , 0.00610352, 0.        ],
           [0.        , 0.        , 0.        , 0.        ]])
    """
    if any(s <= order for s in mu.shape):
        raise ValueError("Shape of image moments must be >= `order`")
    if spacing is None:
        scale = 1.0
    else:
        if isinstance(spacing, cp.ndarray):
            scale = spacing.min()
        else:
            scale = min(spacing)
    if mu.ndim in [2, 3]:
        # compute using in a single kernel for the 2D or 3D cases
        unit_scale = scale == 1.0
        kernel = _get_normalize_kernel(mu.ndim, order, unit_scale)
        nu = cp.full(mu.shape, cp.nan, dtype=mu.dtype)
        # size=1 -> normalization of the moments matrix is being done on a
        # single GPU thread. This should be fine as the size of mu is only
        # ``(order + 1, ) * ndim``.
        kernel(mu, order, scale, nu, size=1)
    else:
        # nu = cp.zeros_like(mu)
        mu0 = mu.ravel()[0]
        coords = cp.meshgrid(
            *((cp.arange(order + 1),) * mu.ndim), indexing='ij', sparse=True
        )
        # broadcast coordinates to get the order of each entry in mu
        power_sum = coords[0]
        for c in coords[1:]:
            power_sum = power_sum + c
        if scale == 1.0:
            nu = _get_nu(mu, power_sum, mu0, mu.ndim)
        else:
            nu = _get_nu_scaled(mu, scale, power_sum, mu0, mu.ndim)
        nu = nu.astype(mu.dtype, copy=False)
    return nu


a = cp.arange(256).reshape(16, 16)

order = 3
scale = 1.0
m = measure.moments(a, order=order)
mn = measure.moments_normalized(m, order=order)

n = cp.full(m.shape, cp.nan)
kernel = _get_normalize_kernel(a.ndim, order, unit_scale=True)
kernel(m, order, scale, n, size=1)

a = cp.arange(512).reshape(8, 8, 8)

order = 3
m = measure.moments(a, order=order)
mn = measure.moments_normalized(m, order=order)

n = cp.full(m.shape, cp.nan)
kernel = _get_normalize_kernel(a.ndim, order, unit_scale=True)
kernel(m, order, scale, n, size=1)
