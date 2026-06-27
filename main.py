import os

from src.registration import (
    load_image,
    save_image,
    build_transform,
    initialize_transform,
    register,
    resample,
    compute_quality_metrics,
)
# from src.segmentation import segment_tumor
# from src.analysis import compare_tumors
# from src.visualization import display_comparison


DATA_DIR = "Data"
RESULTS_DIR = "results"
FIXED_PATH = os.path.join(DATA_DIR, "case6_gre1.nrrd")
MOVING_PATH = os.path.join(DATA_DIR, "case6_gre2.nrrd")

# Paramètres retenus après l'exploration menée dans exploration/
# (voir report/rapport.pdf, section "Méthodologie" pour la justification).
REGISTRATION_METHOD = "rigid"

# # Seed points pour la segmentation semi-automatique (region growing),
# # déterminés manuellement par inspection visuelle des volumes - voir
# # exploration/exploration_segmentation.ipynb pour la démarche.
# SEED_FIXED = (128, 128, 90)   # TODO: ajuster aux vraies coordonnées de la tumeur
# SEED_MOVING = (128, 128, 90)  # idem, dans le volume recalé


def run_registration(fixed, moving):
    print(f"\n[1/4] Recalage ({REGISTRATION_METHOD})...")
    transform = build_transform(REGISTRATION_METHOD)
    transform = initialize_transform(fixed, moving, transform)
    optimized_transform, _, _ = register(fixed, moving, transform)
    registered = resample(fixed, moving, optimized_transform)

    quality = compute_quality_metrics(fixed, registered)
    print(f"   -> MSE={quality['MSE']:.2f}, NCC={quality['NCC']:.4f}")

    save_image(registered, os.path.join(RESULTS_DIR, "registered.nrrd"))
    return registered


# def run_segmentation(fixed, registered_moving):
#     print("\n[2/4] Segmentation des tumeurs...")
#     mask_fixed = segment_tumor(fixed, seed=SEED_FIXED)
#     mask_moving = segment_tumor(registered_moving, seed=SEED_MOVING)

#     save_image(mask_fixed, os.path.join(RESULTS_DIR, "mask_t1.nrrd"))
#     save_image(mask_moving, os.path.join(RESULTS_DIR, "mask_t2.nrrd"))
#     return mask_fixed, mask_moving


# def run_analysis(mask_fixed, mask_moving):
#     print("\n[3/4] Analyse des changements...")
#     report = compare_tumors(mask_fixed, mask_moving)
#     for key, value in report.items():
#         print(f"   - {key}: {value}")
#     return report


# def run_visualization(fixed, registered_moving, mask_fixed, mask_moving):
#     print("\n[4/4] Visualisation (fenêtre interactive VTK)...")
#     display_comparison(fixed, registered_moving, mask_fixed, mask_moving)


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)

    print("Chargement des images...")
    fixed = load_image(FIXED_PATH)
    moving = load_image(MOVING_PATH)

    registered = run_registration(fixed, moving)
    # mask_fixed, mask_moving = run_segmentation(fixed, registered)
    # run_analysis(mask_fixed, mask_moving)
    # run_visualization(fixed, registered, mask_fixed, mask_moving)


if __name__ == "__main__":
    main()