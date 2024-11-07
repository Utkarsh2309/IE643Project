import os
import glob
from PIL import Image, ImageSequence

# Ensure directory exists for combined animations
def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"[INFO] Created directory: {path}")
    else:
        print(f"[INFO] Directory already exists: {path}")

# Combine GIFs across epochs for a specific feature, block, and component
def combine_gifs_across_epochs(feature, block, component, animation_dir, combined_animation_dir):
    epoch_gifs = sorted(glob.glob(os.path.join(animation_dir, f"{feature}_block_{block}_{component}_epoch_*.gif")))
    frames = []

    # Load all frames from each epoch GIF
    for gif_path in epoch_gifs:
        try:
            gif = Image.open(gif_path)
            print(f"[INFO] Loaded GIF for epoch: {gif_path}")
            for frame in ImageSequence.Iterator(gif):
                frames.append(frame.copy())
            gif.close()
        except Exception as e:
            print(f"[ERROR] Failed to load GIF at {gif_path}: {e}")

    # Set path for combined animation and save
    combined_gif_path = os.path.join(combined_animation_dir, f"{feature}_block_{block}_{component}_combined.gif")
    if frames:
        frames[0].save(combined_gif_path, save_all=True, append_images=frames[1:], duration=250, loop=0)
        print(f"[INFO] Combined GIF saved at {combined_gif_path}")
    else:
        print(f"[WARNING] No frames found to combine for {feature} in Block {block}, Component '{component}'")

# Main function to create combined animations for all features and blocks
def generate_combined_animations(animation_dir, combined_animation_dir):
    ensure_dir(combined_animation_dir)
    
    # Features to combine across epochs
    features = ["activations_heatmap", "covariance_heatmap", "gradients_boxplot", "gradients_histogram", "activations_histogram"]
    
    # Loop through blocks and features to create combined animations
    for block in [3, 7]:  # Block 4 and Block 8
        for component in ["attention", "mlp"]:
            for feature in features:
                print(f"[INFO] Combining GIFs for {feature}, Block {block}, Component '{component}'")
                combine_gifs_across_epochs(feature, block, component, animation_dir, combined_animation_dir)

# Define directories for individual animations and combined animations
animation_dir = "./animations"
combined_animation_dir = "./combined_animations_250"
generate_combined_animations(animation_dir, combined_animation_dir)
