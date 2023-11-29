import os

blist = []

# Generate blist with specified criteria
for id_val in range(23):
    color_list = ["red", "orange", "yellow", "light green", "green", "light blue", "blue", "purple", "pink"]
    x_values = list(range(-25, 25, 1))
    y_values = list(range(-25, 25, 1))

    for color in color_list:
        for x_value in x_values:
            for y_value in y_values:
                thisb = dict(
                    id=id_val,
                    color=color,
                    x=x_value,
                    y=y_value
                )
                blist.append(thisb)

output_file_path = os.path.abspath('/Users/knguyen/Documents/Tello/Tello_competitoin/output.txt')

# Write blist to a text file
with open(output_file_path, 'w') as file:
    for item in blist:
        file.write(str(item) + '\n')
