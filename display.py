from rpi_lcd import LCD

lcd = LCD()

def display_clear():
  lcd.clear()

def display(text):
  # Clear the display
  display_clear()
  # Check if the text is too long
  if len(text) > 16:
    # Split the text into two lines
    # Check if we need to split a word
    # If so, put the whole word on the second line
    if text[15] == " ":
      # Split the text
      line1 = text[:15]
      line2 = text[15:]
    else:
      # Split the text at the last space before the 16th character
      split = text[:15].rfind(" ")
      line1 = text[:split]
      line2 = text[split:]

    # Remove the space at the start of the second line, if there is one
    if line2[0] == " ":
      line2 = line2[1:]

    # Display the text
    lcd.text(line1, 1)
    lcd.text(line2, 2)
  else:
    # Display the text
    lcd.text(text, 1)
