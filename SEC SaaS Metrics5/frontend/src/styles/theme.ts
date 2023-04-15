import { ThemeType } from "../types/theme";

export const lightTheme: ThemeType = {
  backgroundColor: "#FCFCFC",
  color: "#2b2f33",
  fontFamily: "'Roboto', sans-serif",

  sidebar: {
    backgroundColor: "#fdfdfd",
    color: "#898d90",
    hoverBackground: "#efefef",
    hoverColor: "#2b2f33",
    themeSwitcherBackground: "#D5EEFF"
  },

  button: {
    backgroundColor: "#D5EEFF",
    color: "#111"
  },

  table: {
    headerColor: "#111"
  }
};

export const darkTheme: ThemeType = {
  backgroundColor: "#111315",
  color: "#fcfcfc",
  fontFamily: "'Roboto', sans-serif",

  sidebar: {
    backgroundColor: "#1a1c1e",
    color: "#85898f",
    hoverBackground: "#272a30",
    hoverColor: "#fcfcfc",
    themeSwitcherBackground: "#D5EEFF"
  },

  button: {
    backgroundColor: "#D5EEFF",
    color: "#111"
  },

  table: {
    headerColor: "#111"
  }
};
