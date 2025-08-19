import argparse
import numpy as np

def parse_args():
    parser = argparse.ArgumentParser(description="Convert Pohang ground truth to PySLAM format")
    parser.add_argument('--input', type=str, required=True, help='Path to input ground truth file')
    parser.add_argument('--output', type=str, default=None, help='Path to output file')
    return parser.parse_args()

def convert_GT(input_path, output_path=None):
    """ Convert Pohang ground truth file to PySLAM format.  
    The input file is expected to have the information of:
    timestamp, pose (x, y, z),orientation (qx, qy, qz, qw) and scale(optional).,

    where the first column is the frame ID and the rest are the pose components.   
    The output has to be in the format:
    timestamp, x, y, z, qx, qy, qz, qw, scale
    """
    data = np.loadtxt(input_path, dtype=np.float64)
    if data.shape[1] < 8:
        raise ValueError("Input data must have at least 8 columns (timestamp, x, y, z, qx, qy, qz, qw).")
    elif data.shape[1] > 9:
        raise ValueError("Input data has too many columns. Expected 8 or 9 columns.")

    # Reorder columns 
    new_order = [0, 5, 6, 7, 1, 2, 3, 4]  # The new order of columns. Change as needed.
    data = data[:, new_order] 

    # Check if the input has scale and add it if not present
    if data.shape[1] == 9:  # If the input has scale
        new_order.append(8)
    elif data.shape[1] == 8:
        scale = 1.0  # Default scale if not provided
        data = np.hstack((data, np.full((data.shape[0], 1), scale)))
    
    # Save the converted data
    if output_path is None:
        output_path = input_path.replace('.txt', '_converted.txt')
    np.savetxt(output_path, data, fmt='%.9f', delimiter='\t')
    

if __name__ == "__main__":
    args = parse_args()
    # You can now use args.input and args.output in your script
    convert_GT(args.input, args.output)
    print(f"Converted ground truth from {args.input} to {args.output if args.output else 'default output file'}")