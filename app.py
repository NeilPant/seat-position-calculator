from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np

app = Flask(__name__)
CORS(app)

# Mapping of enrollment numbers to their corresponding identifiers
all_enroll = {
    "362": 1, "364": 2, "365": 3, "367": 4, "368": 5, "369": 6, "370": 7,
    "371": 8, "372": 9, "373": 10, "374": 11, "375": 12, "376": 13, "377": 14,
    "378": 15, "379": 16, "380": 17, "381": 18, "382": 19, "383": 20,
    "384": 21, "385": 22, "386": 23, "387": 24, "388": 25, "389": 26,
    "390": 27, "394": 28, "395": 29, "398": 30, "399": 31, "400": 32,
    "401": 33, "403": 34, "404": 35, "406": 36, "407": 37, "408": 38,
    "409": 39, "410": 40, "411": 41, "412": 42, "414": 43, "415": 44,
    "416": 45, "417": 46, "418": 47, "419": 48, "420": 49, "421": 50,
    "422": 51, "423": 52, "756": 53, "757": 54, "758": 55
}

# Converts between enrollment numbers and their corresponding identifiers
def convert_to_no(last_3_digits, condition):
    """
    Converts an enrollment number to its identifier or vice versa.
    
    Args:
    - last_3_digits (int): The enrollment number or identifier to convert.
    - condition (bool): If True, convert to identifier. If False, convert to enrollment number.

    Returns:
    - int or str: The corresponding identifier or enrollment number.
    """
    inv_dict = {v: k for k, v in all_enroll.items()}
    if condition:
        return all_enroll.get(str(last_3_digits), -1)
    else:
        return inv_dict.get(last_3_digits, "-1")

# Determines the breakpoints in the data for seat arrangement
def calculate_breakpoints(data_array):
    """
    Finds the breakpoints in the enrollment data based on consecutive enrollment logic.

    Args:
    - data_array (list): A list of enrollment data [enrollNo, class].

    Returns:
    - list: A list of breakpoints [[startEnroll, class]].
    """
    data_array = sorted(data_array, key=lambda x: x[0])
    breakpoints = []
    i = 0
    while i < len(data_array) - 1:
        if data_array[i][0] + 1 == data_array[i + 1][0] and data_array[i][1] != data_array[i + 1][1]:
            breakpoints.append([int(data_array[i + 1][0]), int(data_array[i + 1][1])])
            break
        i += 1

    if breakpoints:
        if int(breakpoints[0][0]) < 25:
            breakpoints.append([int(breakpoints[0][0]) + 30, int(breakpoints[0][1]) + 1])
        elif int(breakpoints[0][0]) > 30:
            breakpoints.append([int(breakpoints[0][0]) - 30, int(breakpoints[0][1]) - 1])

    return breakpoints

# Generates a seating grid based on start position and even/odd logic
def generate_grid(start, is_even):

    arr = [[0 for _ in range(10)] for _ in range(6)]  # Initialize a 6x10 grid with zeros
    current = start

    for col in range(10):  # Iterate over each column
        for row in range(0, 6, 2):  # Fill alternating rows (0, 2, 4)
            if current > 55:  # Stop if the enrollment exceeds the limit
                break
            arr[row][col] = convert_to_no(current, False)
            current += 1

    return arr



# Endpoint to generate grids for a given enrollment number
@app.route('/generate-grid', methods=['POST'])
def generate_grid_endpoint():
    """
    Flask API endpoint to generate the seating grid for a specific enrollment number.

    Request JSON:
    - enrollNo (str): Enrollment number to generate the grid for.

    Response JSON:
    - grid (list): The matching grid.
    - highlight (str): The enrollment number to highlight.
    - class_name (str): The name of the class (e.g., "Class 1").
    """
    try:
        data = request.get_json()
        enroll_no = data.get('enrollNo')

        if enroll_no not in all_enroll:
            return jsonify({"error": f"Enrollment number {enroll_no} not found"}), 400

        data_array = [[int(v), k] for k, v in all_enroll.items()]
        breakpoints = calculate_breakpoints(data_array)

        if not breakpoints:
            return jsonify({"error": "Not enough data to determine breakpoints"}), 400

        for start, is_even in breakpoints:
            grid = generate_grid(start, is_even % 2 == 0)
            for row in grid:
                if enroll_no in row:
                    class_name = f"Class {is_even + 1}"
                    return jsonify({"grid": grid, "highlight": enroll_no, "class_name": class_name})

        return jsonify({"error": f"Enrollment number {enroll_no} not found in any grid"}), 404
    except Exception as e:
        print("Error occurred:", e)
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True)
