

@cp.memoize()
def _get_frangi2d_inner_kernel():

    return cp.ElementwiseKernel(
        in_params='F lambda1, F lambda2, float64 beta_sq, float64 gamma_sq',  # noqa
        out_params='F result',
        operation="""
        F abs_lam1, abs_lam2, r_b, r_g;
        abs_lam1 = abs(lambda1);
        abs_lam2 = abs(lambda2);

        // Compute sensitivity to deviation from a blob-like structure,
        // see equations (10) and (15) in reference [1]_,
        // np.abs(lambda2) in 2D, np.sqrt(np.abs(lambda2 * lambda3)) in 3D
        // CuPy Backend: cp.multiply does not have a reduce method
        // filtered_raw = np.abs(np.multiply.reduce(lambdas))**(1/len(lambdas))
        r_b = abs_lam1 / max(abs_lam2, static_cast<F>(1.0e-10));
        r_b *= r_b;

        // Compute sensitivity to areas of high variance/texture/structure,
        // see equation (12)in reference [1]_
        r_g = lambda1 * lambda1;
        r_g += lambda2 * lambda2;

        // Compute output image for given (sigma) scale.
        // See equations (15) in reference [1]_.
        if (lambda2 == 0.0) {
            // remove background
            result = 0.0;
        } else {
            result = exp(-r_b / beta_sq);
            result *= 1.0 - exp(-r_g / gamma_sq);
        }
        """,
        name='cucim_skimage_filters_frangi2d_inner'
    )


@cp.memoize()
def _get_frangi3d_inner_kernel():

    return cp.ElementwiseKernel(
        in_params='F lambda1, F lambda2, F lambda3, float64 alpha_sq, float64 beta_sq, float64 gamma_sq',  # noqa
        out_params='F result',
        operation="""
        F abs_lam1, abs_lam2, r_a, r_b, r_g;

        abs_lam1 = abs(lambda1);
        abs_lam2 = abs(lambda2);
        abs_lam3 = abs(lambda3);

        // Compute sensitivity to deviation from a plate-like
        // structure (see equations (11) and (15) in reference [1]_).
        r_a = abs_lam2 / max(abs_lam3, static_cast<F>(1.0e-10));
        r_a *= r_a;

        // Compute sensitivity to deviation from a blob-like structure,
        // see equations (10) and (15) in reference [1]_,
        // np.abs(lambda2) in 2D, np.sqrt(np.abs(lambda2 * lambda3)) in 3D
        // CuPy Backend: cp.multiply does not have a reduce method
        // filtered_raw = np.abs(np.multiply.reduce(lambdas))**(1/len(lambdas))
        r_b = (abs_lam1 * abs_lam1) / max(abs_lam2 * abs_lam3, static_cast<F>(1.0e-10));

        // Compute sensitivity to areas of high variance/texture/structure,
        // see equation (12)in reference [1]_
        r_g = lambda1 * lambda1;
        r_g += lambda2 * lambda2;
        r_g += lambda3 * lambda3;

        // Compute output image for given (sigma) scale.
        // See equations (13) in reference [1]_.
        if (max(lambda2, lambda3) == 0) {
            // remove background
            result = 0.0;
        } else {
            result = 1.0 - exp(-r_a / alpha_sq);
            result *= exp(-r_b / beta_sq);
            result *= 1.0 - exp(-r_g / gamma_sq);
        }
        """,
        name='cucim_skimage_filters_frangi3d_inner'
    )


def frangi(image, sigmas=range(1, 10, 2), scale_range=None,
           scale_step=None, alpha=0.5, beta=0.5, gamma=15,
           black_ridges=True, mode='reflect', cval=0):
    """
    Filter an image with the Frangi vesselness filter.

    This filter can be used to detect continuous ridges, e.g. vessels,
    wrinkles, rivers. It can be used to calculate the fraction of the
    whole image containing such objects.

    Defined only for 2-D and 3-D images. Calculates the eigenvectors of the
    Hessian to compute the similarity of an image region to vessels, according
    to the method described in [1]_.

    Parameters
    ----------
    image : (N, M[, P]) ndarray
        Array with input image data.
    sigmas : iterable of floats, optional
        Sigmas used as scales of filter, i.e.,
        np.arange(scale_range[0], scale_range[1], scale_step)
    scale_range : 2-tuple of floats, optional
        The range of sigmas used.
    scale_step : float, optional
        Step size between sigmas.
    alpha : float, optional
        Frangi correction constant that adjusts the filter's
        sensitivity to deviation from a plate-like structure.
    beta : float, optional
        Frangi correction constant that adjusts the filter's
        sensitivity to deviation from a blob-like structure.
    gamma : float, optional
        Frangi correction constant that adjusts the filter's
        sensitivity to areas of high variance/texture/structure.
    black_ridges : boolean, optional
        When True (the default), the filter detects black ridges; when
        False, it detects white ridges.
    mode : {'constant', 'reflect', 'wrap', 'nearest', 'mirror'}, optional
        How to handle values outside the image borders.
    cval : float, optional
        Used in conjunction with mode 'constant', the value outside
        the image boundaries.

    Returns
    -------
    out : (N, M[, P]) ndarray
        Filtered image (maximum of pixels across all scales).

    Notes
    -----
    Written by Marc Schrijver, November 2001
    Re-Written by D. J. Kroon, University of Twente, May 2009, [2]_
    Adoption of 3D version from D. G. Ellis, Januar 20017, [3]_

    See also
    --------
    meijering
    sato
    hessian

    References
    ----------
    .. [1] Frangi, A. F., Niessen, W. J., Vincken, K. L., & Viergever, M. A.
        (1998,). Multiscale vessel enhancement filtering. In International
        Conference on Medical Image Computing and Computer-Assisted
        Intervention (pp. 130-137). Springer Berlin Heidelberg.
        :DOI:`10.1007/BFb0056195`
    .. [2] Kroon, D. J.: Hessian based Frangi vesselness filter.
    .. [3] Ellis, D. G.: https://github.com/ellisdg/frangi3d/tree/master/frangi
    """
    if scale_range is not None and scale_step is not None:
        warn('Use keyword parameter `sigmas` instead of `scale_range` and '
             '`scale_range` which will be removed in version 0.17.',
             stacklevel=2)
        sigmas = np.arange(scale_range[0], scale_range[1], scale_step)

    # Check image dimensions
    check_nD(image, [2, 3])

    # Check (sigma) scales
    sigmas = _check_sigmas(sigmas)

    # Rescale filter parameters
    alpha_sq = 2 * alpha ** 2
    beta_sq = 2 * beta ** 2
    gamma_sq = 2 * gamma ** 2

    # Get image dimensions
    ndim = image.ndim

    # Invert image to detect dark ridges on light background
    if black_ridges:
        image = invert(image)

    float_dtype = _supported_float_type(image.dtype)

    filtered_array = cp.empty(image.shape, dtype=float_dtype)

    if ndim == 2:
        inner_kernel = _get_frangi2d_inner_kernel()
    elif ndim == 3:
        inner_kernel = _get_frangi3d_inner_kernel()

    # Filtering for all (sigma) scales
    for i, sigma in enumerate(sigmas):

        # Calculate (abs sorted) eigenvalues
        lambda1, *lambdas = compute_hessian_eigenvalues(image, sigma,
                                                        sorting='abs',
                                                        mode=mode, cval=cval)
        if ndim == 2:
            lambda2 = lambdas[0]
            inner_kernel(
                lambda1, lambda2, beta_sq, gamma_sq, filtered_array
            )
        else:
            lambda2 = lambdas[0]
            lambda3 = lambdas[1]
            inner_kernel(
                lambda1, lambda2, lambda3, alpha_sq, beta_sq, gamma_sq,
                filtered_array
            )
        # Return for every pixel the maximum value over all (sigma) scales
        if i == 0:
            filtered_max = filtered_array.copy()
        else:
            filtered_max = cp.maximum(filtered_array, filtered_max)
    return filtered_max

