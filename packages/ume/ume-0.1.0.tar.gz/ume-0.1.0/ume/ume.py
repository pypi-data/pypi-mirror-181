import re
from hashlib import sha256

import pytesseract
from imagehash import phash, average_hash, dhash, whash, colorhash, crop_resistant_hash
from sewar import mse, rmse, psnr, rmse_sw, uqi, ssim, ergas, scc, rase, sam, msssim, vifp, psnrb

from .utils import classproperty, returns, sewar_patcher, image_hash_patcher, get_pil_image, AttrDict


class QualityMetrics:
    mse = staticmethod(sewar_patcher(mse))
    rmse = staticmethod(sewar_patcher(rmse))
    psnr = staticmethod(sewar_patcher(psnr))
    rmse_sw = staticmethod(sewar_patcher(rmse_sw))
    uqi = staticmethod(sewar_patcher(uqi))
    ssim = staticmethod(sewar_patcher(ssim))
    ergas = staticmethod(sewar_patcher(ergas))
    scc = staticmethod(sewar_patcher(scc))
    rase = staticmethod(sewar_patcher(rase))
    sam = staticmethod(sewar_patcher(sam))
    msssim = staticmethod(sewar_patcher(msssim))
    vifp = staticmethod(sewar_patcher(vifp))
    psnrb = staticmethod(sewar_patcher(psnrb))


class ImageHashers:
    phash = staticmethod(image_hash_patcher(phash))
    average_hash = staticmethod(image_hash_patcher(average_hash))
    dhash = staticmethod(image_hash_patcher(dhash))
    whash = staticmethod(image_hash_patcher(whash))
    colorhash = staticmethod(image_hash_patcher(colorhash))
    crop_resistant_hash = staticmethod(image_hash_patcher(crop_resistant_hash))


class Utilities:
    @staticmethod
    @get_pil_image.apply_params
    def get_text_from_image(image, input_type):
        image = get_pil_image(image, input_type)
        return Utilities.normalize_text(pytesseract.image_to_string(image))

    @staticmethod
    @get_pil_image.apply_params
    def cryptographic_hash(image, input_type, hasher=sha256):
        image = get_pil_image(image, input_type)
        return hasher(image.tobytes()).hexdigest()

    @staticmethod
    def normalize_text(text):
        return re.sub(r"\W+", " ", text)


class UniqueMemeEngine:
    """
    Usage:
       For quality metrics:
           ume.quality_metrics.mse(img1, img2, image_source)
    """

    input_type = AttrDict.from_data(get_pil_image.params_dict)
    quality_metrics = classproperty(returns(QualityMetrics))
    image_hashers = classproperty(returns(ImageHashers))
    utilities = classproperty(returns(Utilities))


ume = UniqueMemeEngine  # A nice alias
