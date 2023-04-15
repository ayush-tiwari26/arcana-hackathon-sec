import React from "react";
import { BrowserRouter } from "react-router-dom";
import styled, { ThemeProvider } from "styled-components";
import Navbar from "./components/Navbar";
import { SearchProvider } from "./hooks/useSearchContext";
import GlobalStyles from "./styles/GlobalStyles";
import { lightTheme } from "./styles/theme";
import Switch from "./Switch";

const AppContainer = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 100%;
`;

function App() {
  return (
    <BrowserRouter>
      <SearchProvider>
        <ThemeProvider theme={lightTheme}>
          <GlobalStyles />
          <AppContainer>
            <Switch />
          </AppContainer>
        </ThemeProvider>
      </SearchProvider>
    </BrowserRouter>
  );
}

export default App;
