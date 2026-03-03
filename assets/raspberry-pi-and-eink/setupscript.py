"""
ePaper Display text coming from a serial port using the Pillow Library.

Based on the python scripts from https://learn.adafruit.com/2-13-in-e-ink-bonnet/usage
modified for this particular use case

ASSUMES:
- connected to SSD1680Z e-ink bonnet
- screen is black and white
- there is a serial port connected on a USB
- Installed CircuitPython Blinka library from adafruit https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi
- script is running on raspberry pi zero. Has not been tested on other raspberry pi systems (though should work...)

"""

import board
import busio
import digitalio
from PIL import Image, ImageDraw, ImageFont
from adafruit_epd.epd import Adafruit_EPD
import serial
import time
import serial.tools.list_ports


from adafruit_epd.ssd1680 import Adafruit_SSD1680Z


# First define some color constants
WHITE = (0xFF, 0xFF, 0xFF)
BLACK = (0x00, 0x00, 0x00)

# Next define some constants to allow easy resizing of shapes and colors
BORDER = 5
FONTSIZE = 18
FONT_MAX_LENGTH = 27
BACKGROUND_COLOR = WHITE
TEXT_COLOR = BLACK


# create the spi device and pins we will need
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
ecs = digitalio.DigitalInOut(board.CE0)
dc = digitalio.DigitalInOut(board.D22)
rst = digitalio.DigitalInOut(board.D27)
busy = digitalio.DigitalInOut(board.D17)
srcs = None


# e ink display
display = Adafruit_SSD1680Z(122, 250, spi, cs_pin=ecs, dc_pin=dc, sramcs_pin=srcs,
                          rst_pin=rst, busy_pin=busy)


display.rotation = 1

# replace some space with a newline character so the string will fit on
# the given screen. NOTE: does not have a max number of rows check
def reformat_text(text: str, maxlength: int):
    new_string = ""
    cur_row_length = 0
    for word in text.split(' '):
        if cur_row_length + len(word) < maxlength:
            if len(new_string) == 0:
                new_string = word
                cur_row_length = len(word)
            else:
                new_string = new_string + " " + word
                cur_row_length += len(word) + 1
        else:
            new_string = new_string + "\n" + word
            cur_row_length = len(word)
    return new_string

# re-draw the entire screen with the new text message
def display_text( text: str):
    image = Image.new("RGB", (display.width, display.height), WHITE)

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    # Draw a filled box as the background
    draw.rectangle(
        (0, 0, display.width - 1, display.height - 1),
        fill=BACKGROUND_COLOR,
    )

    # Load a TTF Font
    # NOTE: linux systems normally default have this font
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", FONTSIZE)

    # Draw the text after its been reformated
    new_text = reformat_text(text, FONT_MAX_LENGTH)
    draw.text(
    (BORDER, BORDER),
    new_text,
    font=font,
    fill=TEXT_COLOR,
    )

    # Display image.
    display.image(image)
    display.display()

def process_serial_stream(ser, line_processor):
    """Process continuous serial data stream"""
    line_buffer = b''
    
    while True:
        try:
            # Read available data
            if ser.in_waiting:
                chunk = ser.read(ser.in_waiting)
                line_buffer += chunk
                
                # Process complete lines
                while b'\n' in line_buffer:
                    line, line_buffer = line_buffer.split(b'\n', 1)
                    try:
                        text = line.decode('utf-8').strip()
                        if text:
                            result = line_processor(text)
                            if result:
                                yield result
                    except Exception as e:
                        print(f"Process error: {e}")
            else:
                time.sleep(0.001)
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Stream error: {e}")

def parse_msg(line):
    """check if it was a detection, and return if so"""
    # for testing just return it all
    # TODO can add filtering here if the line is something we dont want to print
    # e.g. only print lines that say "DEBUG" or "ERR" in them
    return line

print("Booting up...")
display_text(f"{time.strftime("[%H:%M:%S]")} Booting up...")
last_display_update = time.time()
# trigger serial tracking
last_serial_string = ""
try:

    #find espressif connected board
    #TODO if connected dev board is diff, need to update the PID/VID here
    portname = ""
    for p in serial.tools.list_ports.comports():
        if p.pid == 4097 and p.vid == 12346:
            portname = p.device

    if portname == "":
        print("CANT FIND PORT")
    else:
        print(f"Found port {portname}, connecting...")
        # assumes connection is 115200 baud rate
        # TODO update baudrate if needed
        with serial.Serial(portname, 115200, timeout=1) as ser:
            for detection in process_serial_stream(ser, parse_msg):
                print(f"detected string: {detection}")
                # print all new messages, and if it's been the same message for over 60 seconds
                # (e.g. the same status message of "scanning" or something)
                # print the same message but with updated timestamp, to show its not dead
                if (last_serial_string != detection or (time.time() - last_display_update) > 60):
                    display_text(f"{time.strftime("[%H:%M:%S]")} {detection}")
                    last_serial_string = detection
                    last_display_update = time.time()
                    
except Exception as e:
    print(f"Serial connection failed {e}")
