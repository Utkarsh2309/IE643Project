import os
import h5py
import numpy as np
import matplotlib.pyplot as plt

# Set up directories for saving plots
def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

# Function to plot and save box plot for gradients
def plot_boxplot(data, title, xlabel, ylabel, save_path):
    plt.figure(figsize=(10, 6))
    plt.boxplot(data, vert=False, patch_artist=True, notch=True)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

# Visualization code to extract and plot gradients as box plots from HDF5
def visualize_gradients_boxplot(hdf5_path, output_dir):
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

                        # Plot Gradients Box Plot
                        if "gradients" in batch_group:
                            gradients = batch_group["gradients"][:]
                            # Flatten gradients to 1D for plotting
                            gradients = gradients.flatten()
                            plot_boxplot(
                                gradients,
                                title=f"{plot_title_prefix} Gradients Box Plot",
                                xlabel="Gradient Values",
                                ylabel="Distribution",
                                save_path=os.path.join(plot_dir, "gradients_boxplot.png")
                            )

# Run visualization for gradients box plot
hdf5_path = "./training_data.h5"
output_dir = "./plots_gradients_boxplots"
visualize_gradients_boxplot(hdf5_path, output_dir)
