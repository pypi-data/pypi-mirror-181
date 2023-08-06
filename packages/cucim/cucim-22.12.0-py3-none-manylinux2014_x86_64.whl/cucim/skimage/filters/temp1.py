        alpha = 1 / (image.ndim + 1)

    # tiny matrix, so just use a single threaded kernel to assign the values
    circulant_init_kernel = _get_circulant_init_kernel(image.ndim, alpha)
    mtx = cp.empty((image.ndim, image.ndim), dtype=image.dtype)
    circulant_init_kernel(mtx, size=1)

    # Generate empty array for storing maximum value
    # from different (sigma) scales
    filtered_max = cp.zeros_like(image)
    for sigma in sigmas:  # Filter for all sigmas.
        eigvals = hessian_matrix_eigvals(hessian_matrix(
            image, sigma, mode=mode, cval=cval, use_gaussian_derivatives=True))

        # cucim's hessian_matrix differs numerically from the one in skimage.
        # Sometimes where skimage returns 0, it returns very small values
        # (1e-15-1e-14). Here we set values < 1e-12 to 0 to better replicate
        # the same behavior.
        eigvals[abs(eigvals) < 1e-12] = 0.0

        # Compute normalized eigenvalues l_i = e_i + sum_{j!=i} alpha * e_j.
        vals = cp.tensordot(mtx, eigvals, 1)
        # Get largest normalized eigenvalue (by magnitude) at each pixel.
        vals = cp.take_along_axis(
            vals, abs(vals).argmax(0)[None], 0).squeeze(0)
        # Remove negative values.
        vals = cp.maximum(vals, 0)
        # Normalize to max = 1 (unless everything is already zero).
        max_val = vals.max()
        if max_val > 0:
            vals /= max_val
        filtered_max = cp.maximum(filtered_max, vals)
        # print(f"{black_ridges=}, {image.max()=}, {sigma=}, {filtered_max=}")

    return filtered_max  # Return pixel-wise max over all sigmas.