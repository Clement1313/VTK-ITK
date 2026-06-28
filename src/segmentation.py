import itk
import numpy as np

Dimension = 3
PixelType = itk.F
ImageType = itk.Image[PixelType, Dimension]
_BinType = itk.Image[itk.SS, Dimension]
_LblType = itk.Image[itk.UL, Dimension]


def segment_tumor(image, seed, lower_threshold=700):
    """
    Segmentation par seuillage + composante connexe.

    On seuille l'image pour ne garder que les voxels hyperintenses,
    puis on extrait la composante connexe contenant le seed point.
    Le seuil a été déterminé par inspection visuelle (cf. rapport).

    seed            : (x, y, z) en coordonnées voxel ITK.
    lower_threshold : seuil bas d'intensité — voxels en dessous exclus.
    """
    arr = itk.array_from_image(image)

    # seuillage binaire
    bin_arr = (arr >= lower_threshold).astype(np.int16)
    bin_img = itk.image_from_array(bin_arr)
    bin_img.CopyInformation(image)

    # étiquetage des composantes connexes
    cc = itk.ConnectedComponentImageFilter[_BinType, _LblType].New()
    cc.SetInput(bin_img)
    cc.Update()

    # garder uniquement la composante qui contient le seed
    label_arr = itk.array_from_image(cc.GetOutput())
    seed_label = int(label_arr[seed[2], seed[1], seed[0]])

    if seed_label == 0:
        raise ValueError(
            f"Le seed {seed} est hors du masque (intensité {arr[seed[2],seed[1],seed[0]]:.0f} "
            f"< seuil {lower_threshold}). Diminuer lower_threshold ou ajuster le seed."
        )

    mask_arr = (label_arr == seed_label).astype(np.uint8)
    mask = itk.image_from_array(mask_arr)
    mask.CopyInformation(image)
    mask.DisconnectPipeline()
    return mask


def count_voxels(mask):
    arr = itk.array_from_image(mask)
    return int((arr > 0).sum())


def voxel_volume_mm3(mask):
    spacing = mask.GetSpacing()
    return float(spacing[0] * spacing[1] * spacing[2])


def save_mask(mask, filename):
    itk.imwrite(mask, filename)
