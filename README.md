# GRID Car Specs Adjustment Script

This Python script is used to adjust the specifications of cars in the 2008 game, GRID. It compares the specifications of a chosen car with another car (which can be chosen randomly or specified), and adjusts the specifications of the chosen car based on the difference.  This can create some interesting results!  

## Why?

I love GRID and wanted to add a little bit of customization.  I was originally hoping to discover what each car value in their CSVs are for, but couldn't find a reference to which number did what.  So instead I threw a chaos monkey wrench into the mix and made this script to just go crazy on changing values willy nilly.  It's been fun.

## How it works

GRID saves each car's values/specifications as a csv.  These CSVs are located in the each car folder in the 'cars' folder of your GRID installation.  These values/specifications control things like gear shift timings, braking, cornering, steer assist, aerodynamics, weight, RPM limits and so much more. GRID loads these vehicle CSV files right as you join a race.  NOT when a race restart happens.  Only when you're coming from the menu and going into a race.  

In the GRID 'cars' folder are the abbreviations of the vehicles.  Sometimes you gotta guess which one is which.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.


### Prerequisites

Running GRID from Steam ( not totally required )
You need Python 3.x and the following Python libraries installed:

- csv
- random
- glob
- time
- os

### Installation

0. Open a powershell window.
1. Clone the repo: `git clone https://github.com/milagrofrost/grid_car_spec_chaos.git`
2. Change into the directory: `cd grid_car_spec_chaos`


## Usage

You can adjust the following parameters in the script 'update_specs.py':

- `car_to_adjust`: The target car to adjust. Set to the car abbreviation.
- `car_to_diff`: The car to compare against. Set to "random" to use a random car from the cars folder, otherwise set to the car abbreviation.
- `inc_dec`: The amount to increase or decrease a value by. 0.9 = 90% of the original value.
- `odds`: Chance of adjusting a value.
- `index_range_modifier`: A list of indexes to adjust. Can be a single number or a range.
- `grid_cars_path`: path to the Grid cars folder This is my path.  Change it to yours.  use double backslashes
- `grid_screenshot_path`: path to the Grid screenshots folder '56736994' is my steam id.  Change it to yours.  use double backslashes

Make sure to first update your GRID installation path variable and also change the screenshot path to one that is specific to your installation.

Open a powershell window.
Run the script with: `python update_specs.py`

The script at initial load will go ahead and update the values for your target vehicle you want to adjust.   YOu can verify the values were updated by going to the car CSV file in your GRID installation and make sure it was last modified very recently.  

After that, the script will continue to run forever.  I watches the screenshot folder every few seconds, waiting for any new screenshots to arrive.  When it sees a new screenshot from GRID, using Steam's 'F12' hotkey, it will create a new set of values.  After that you'll need to retire your race and start again to load the new values.  I used this screen show method as a way to interact with python script without having to switch between game and the window where python is running.  

## License

This project is licensed under the MIT License - see the LICENSE.md file for details

## Acknowledgments

- Github Co-pilot for help in auto-completing code.  