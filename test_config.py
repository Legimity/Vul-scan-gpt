import configparser

# Create a ConfigParser object
config = configparser.ConfigParser()

# Read the conf.ini file
config.read('conf/conf.ini')

# Access the save_path value
save_path = config['save']['save_path']

print(f"The save path is: {save_path}")

# Example usage: Saving a file to the specified path
with open(f"{save_path}output.txt", "w") as file:
    file.write("This is a test file.")
