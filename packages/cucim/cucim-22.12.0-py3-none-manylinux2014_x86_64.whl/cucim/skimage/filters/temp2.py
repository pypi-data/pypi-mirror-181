        alpha = 1.0 / ndim

    # Invert image to detect dark ridges on bright background
    if black_ridges:
        image = invert(image)

    float_dtype = _supported_float_type(image.dtype)
    image = image.astype(float_dtype, copy=False)

    # Generate empty (n+1)D arrays for storing auxiliary images filtered at
    # different (sigma) scales
    filtered_array = cp.empty(sigmas.shape + image.shape, dtype=float_dtype)

    # Filtering for all (sigma) scales
    for i, sigma in enumerate(sigmas):

        # Calculate (sorted) eigenvalues
        eigenvalues = compute_hessian_eigenvalues(image, sigma, sorting='abs',
                                                  mode=mode, cval=cval)
        # CuPy Backend: do intermediate computations with tiny arrays on the
        #               CPU
        # TODO: refactor to avoid host-device transfer
        eigenvalues = cp.asnumpy(eigenvalues)

        if ndim > 1:

            # Set coefficients for scaling eigenvalues
            coefficients = [alpha] * ndim
            coefficients[0] = 1

            # Compute normalized eigenvalues l_i = e_i + sum_{j!=i} alpha * e_j
            auxiliary = [np.sum([eigenvalues[i] * np.roll(coefficients, j)[i]
                         for j in range(ndim)], axis=0) for i in range(ndim)]

            # Get maximum eigenvalues by magnitude
            auxiliary = auxiliary[-1]
            auxiliary = cp.asarray(auxiliary)

            # Rescale image intensity and avoid ZeroDivisionError
            filtered = _divide_nonzero(auxiliary, cp.min(auxiliary))

            # Remove background
            filtered = cp.where(auxiliary < 0, filtered, 0)

            # Store results in (n+1)D matrices
            filtered_array[i] = filtered

    # Return for every pixel the maximum value over all (sigma) scales
    return cp.max(filtered_array, axis=0)