import { createGlobalStyle } from "styled-components";
import { ThemeType } from "../types/theme";

const GlobalStyles = createGlobalStyle<{ theme: ThemeType }>`
  body {
    margin: 0;
    background-color: ${(props) => props.theme.backgroundColor};
    color: ${(props) => props.theme.color};
    transition: all 0.35s ease-in-out 0s;
    font-size: 20px;
    font-family: ${(props) => props.theme.fontFamily};
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;

    .basic-single .select__control {
      padding: 0.3rem 1rem;
      background: #ffffff;
      border: 1px solid #efefef;
      box-sizing: border-box;
      border-radius: 8px;
      font-size: 1.1rem;
      margin: 0 0.5rem;
      min-width: 300px;
    }
  }
`;

export default GlobalStyles;
