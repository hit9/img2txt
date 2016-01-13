def alpha_blend(src, dst):
    # Does not assume that dst is fully opaque
    # See https://en.wikipedia.org/wiki/Alpha_compositing - section on "Alpha Blending"
    src_multiplier = (src[3] / 255.0)
    dst_multiplier = (dst[3] / 255.0) * (1 - src_multiplier)
    result_alpha = src_multiplier + dst_multiplier
    if result_alpha == 0:       # special case to prevent div by zero below
        return (0, 0, 0, 0)
    else:
        return (
            int(((src[0] * src_multiplier) + (dst[0] * dst_multiplier)) / result_alpha), 
            int(((src[1] * src_multiplier) + (dst[1] * dst_multiplier)) / result_alpha),
            int(((src[2] * src_multiplier) + (dst[2] * dst_multiplier)) / result_alpha),
            int(result_alpha * 255) 
        ) 
           
