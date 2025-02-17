from style import COLORS, colortest

if __name__ == "__main__":
    print("Testing default colors:")
    colortest()

    print("\nTesting compatible colors:")
    COLORS.use_compatible_colors()
    colortest()