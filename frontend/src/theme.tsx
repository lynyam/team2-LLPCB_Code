import {
  MantineTheme,
  MantineThemeColorsOverride,
  MantineThemeOverride,
} from "@mantine/core";

const colors: MantineThemeColorsOverride = {
  gray: [
    "#F8F9FA", // Almost white
    "#E9ECEF", // Light gray
    "#DEE2E6", // Mid light gray
    "#CED4DA", // Neutral gray
    "#ADB5BD", // Slightly darker gray
    "#868E96", // Darker mid-gray
    "#495057", // Dark gray
    "#343A40", // Darker gray
    "#212529", // Almost black
    "#121416", // Deepest black-like tone
  ],
  blue: [
    "#EDF2F7", // Light muted blue
    "#DBE2EB",
    "#B6C4D4",
    "#92A6BE",
    "#6D88A7",
    "#486A91",
    "#2D4C74",
    "#1F3657",
    "#14233A",
    "#0C1523", // Deep blue-black
  ],
  sepia: [
    "#FDF6E3", // Light sepia
    "#FAEAC1",
    "#F3D79A",
    "#E9C075",
    "#D4A054",
    "#B6823C",
    "#90662A",
    "#6A4B1D",
    "#452F10",
    "#2C1D0A", // Deep sepia-brown
  ],
};

const newspaperTheme: MantineThemeOverride = {
  primaryColor: "gray",
  fontFamily: "Georgia, serif", // Classic serif font for a newspaper feel
  colors,

  components: {
    Button: {
      defaultProps: {
        color: "gray.9",
      },
    },
  },
};

export default newspaperTheme;
