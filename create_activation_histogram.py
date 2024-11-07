import os
import h5py
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set up directories for saving plots
def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

# Modify the plot_histogram function to handle higher-dimensional data
def plot_histogram(data, title, xlabel, ylabel, save_path):
    if data.ndim > 1:
        data = data.flatten()  # Flatten to 1D to plot histogram
    plt.figure(figsize=(8, 6))
    plt.hist(data, bins=30, color='blue', alpha=0.7)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()


# Function to plot and save heatmap
# Modify the plot_heatmap function to handle 3D data by averaging over the first dimension
# def plot_heatmap(data, title, save_path):
#     if data.ndim == 3:
#         data = np.mean(data, axis=0)  # Average over the batch dimension
#     plt.figure(figsize=(10, 8))
#     sns.heatmap(data, cmap='viridis')
#     plt.title(title)
#     plt.tight_layout()
#     plt.savefig(save_path)
#     plt.close()


# Visualization code to extract and plot data from HDF5
def visualize_hdf5_data(hdf5_path, output_dir):
    with h5py.File(hdf5_path, 'r') as hdf5_file:
        for epoch in hdf5_file.keys():
            epoch_group = hdf5_file[epoch]
            for block in epoch_group.keys():
                block_group = epoch_group[block]
                for component in block_group.keys():
                    component_group = block_group[component]
                    for batch in component_group.keys():
                        batch_group = component_group[batch]
                        
                        # Set up directories for saving plots
                        plot_dir = os.path.join(output_dir, epoch, block, component, batch)
                        ensure_dir(plot_dir)
                        
                        # Titles and file naming for plots
                        epoch_num = epoch.split('_')[1]
                        block_num = block.split('_')[2]
                        batch_num = batch.split('_')[1]
                        plot_title_prefix = f"Epoch {epoch_num} | Block {block_num} | Batch {batch_num} - {component.capitalize()}"

                        # Plot Weights Histogram (Commented out as requested)
                        # if "weights" in batch_group:
                        #     weights = batch_group["weights"][:]
                        #     plot_histogram(
                        #         weights,
                        #         title=f"{plot_title_prefix} Weights Distribution",
                        #         xlabel="Weight Values",
                        #         ylabel="Frequency",
                        #         save_path=os.path.join(plot_dir, "weights_histogram.png")
                        #     )

                        # Plot Activations Heatmap
                        # if "activations" in batch_group:
                        #     activations = batch_group["activations"][:]
                        #     plot_heatmap(
                        #         activations,
                        #         title=f"{plot_title_prefix} Activations Heatmap",
                        #         save_path=os.path.join(plot_dir, "activations_heatmap.png")
                        #     )

                        # # Plot Covariance Matrix Heatmap
                        # if "covariance_matrix" in batch_group:
                        #     covariance_matrix = batch_group["covariance_matrix"][:]
                        #     plot_heatmap(
                        #         covariance_matrix,
                        #         title=f"{plot_title_prefix} Covariance Matrix Heatmap",
                        #         save_path=os.path.join(plot_dir, "covariance_heatmap.png")
                        #     )

                        # Plot Gradients Histogram
                        if "activations" in batch_group:
                            activations = batch_group["activations"][:]
                            plot_histogram(
                                activations,
                                title=f"{plot_title_prefix} Activation Distribution",
                                xlabel="Activation Values",
                                ylabel="Frequency",
                                save_path=os.path.join(plot_dir, "activations_histogram.png")
                            )

# Run visualization
hdf5_path = "./training_data.h5"
output_dir = "./plots"
visualize_hdf5_data(hdf5_path, output_dir)
