import os
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from PIL import Image
import glob

# Function to ensure directory exists
def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"[INFO] Created directory: {path}")
    else:
        print(f"[INFO] Directory already exists: {path}")

# Function to load images across all batch folders for a specific feature, block, component, and epoch
def load_images_for_feature(feature, block, component, epoch_path):
    images = []
    # Use glob to find all batch folders and the specific feature images within them
    batch_folders = sorted(glob.glob(os.path.join(epoch_path, f'encoder_block_{block}', component, 'batch_*')))
    print(f"[DEBUG] Searching images for '{feature}' in Block {block}, Component '{component}' within epoch {epoch_path}")

    for batch_folder in batch_folders:
        feature_image_path = os.path.join(batch_folder, f"{feature}.png")
        
        # Check if the feature plot exists for this batch
        if os.path.exists(feature_image_path):
            try:
                img = Image.open(feature_image_path)
                images.append(img)
                print(f"[DEBUG] Loaded image: {feature_image_path}")
            except Exception as e:
                print(f"[ERROR] Failed to load image at {feature_image_path}: {e}")
        else:
            print(f"[WARNING] Image not found: {feature_image_path}")
    
    # Final check on images loaded
    if images:
        print(f"[INFO] Successfully loaded {len(images)} images for '{feature}' in Block {block}, Component '{component}'")
    else:
        print(f"[WARNING] No images found for '{feature}' in Block {block}, Component '{component}' within {epoch_path}")
    
    return images

# Function to create animation from a list of images
def create_animation(images, save_path, interval=500):
    fig, ax = plt.subplots()
    plt.axis('off')  # Turn off axis for cleaner animation display

    ims = []
    for img in images:
        im = plt.imshow(img, animated=True)
        ims.append([im])

    ani = animation.ArtistAnimation(fig, ims, interval=interval, blit=True)

    # Save animation
    try:
        ani.save(save_path, writer='pillow')
        print(f"[INFO] Animation saved successfully at {save_path}")
    except Exception as e:
        print(f"[ERROR] Failed to save animation at {save_path}: {e}")

# Main function to create animations for all features and blocks
def generate_animations(plot_dir, animation_dir):
    ensure_dir(animation_dir)
    
    # Feature types to animate
    features = ["activations_histogram"]
    
    # Loop through blocks and features to create animations
    for block in [3, 7]:  # Block 4 and Block 8
        for component in ["attention", "mlp"]:
            for feature in features:
                # For each epoch, collect images across batches
                epoch_folders = sorted(os.listdir(plot_dir))
                for epoch in epoch_folders:
                    epoch_path = os.path.join(plot_dir, epoch)
                    images = load_images_for_feature(feature, block, component, epoch_path)
                    
                    # Set animation save path for each epoch
                    save_path = os.path.join(animation_dir, f"{feature}_block_{block}_{component}_epoch_{epoch}.gif")
                    
                    # Create animation if images are found
                    if images:
                        create_animation(images, save_path)
                    else:
                        print(f"[WARNING] Skipping animation for '{feature}' in Block {block}, Component '{component}', Epoch {epoch} due to missing images.")

            # Animation for weights (Commented out as requested)
            # weight_images = load_images_for_feature("weights_boxplot", block, component, epoch_path)
            # weight_save_path = os.path.join(animation_dir, f"weights_boxplot_block_{block}_{component}_epoch_{epoch}.gif")
            # if weight_images:
            #     create_animation(weight_images, weight_save_path)
            #     print(f"[INFO] Weights Animation saved: {weight_save_path}")

# Define directories for plots and animations
plot_dir = "./plots"
animation_dir = "./animations"
generate_animations(plot_dir, animation_dir)
