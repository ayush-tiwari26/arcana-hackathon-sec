import React, { useEffect, useState } from "react";
import {
  ChevronLeft,
  ChevronRight,
  Terminal,
  BarChart2,
  CreditCard,
  Sidebar as SidebarIcon,
  Sun,
  Moon
} from "react-feather";
import { useNavigate } from "react-router-dom";
import styled from "styled-components";
import { SidebarOption } from "../types/company";
import { navbarOptions } from "../utils/constants";

//----------------Styled Components---------------

const Container = styled.div`
  display: flex;
  flex-direction: column;
  position: relative;
  position: sticky;
  top: 1rem;
  background-color: ${(props) => props.theme.sidebar.backgroundColor};
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.15);
  padding: 0 1rem;
`;

const List = styled.ul`
  display: flex;
  flex-direction: column;
  list-style-type: none;
  margin: 0;
  padding: 0;
  margin: 0.5rem 1rem;
`;

const Icon = styled.img`
  margin: 0 0.5rem;
  width: 25px;
  aspect-ratio: 1/1;
  color: ${(props) => props.theme.sidebar.color};
`;

// TODO: inline optional props not working for some reason
const ListItem = styled.li<{ active: boolean }>`
  display: flex;
  align-items: center;
  white-space: nowrap;
  position: relative;
  padding: 0.5rem 1rem;
  margin: 0.25rem 0;
  font-size: 1rem;

  cursor: pointer;
  border-radius: 10px;
  color: ${(props) => props.theme.sidebar.color};
  background-color: ${(props) => (props.active ? "#d5eeff" : "transparent")};

  &:hover {
    background-color: #d5eeff;
    color: ${(props) => props.theme.sidebar.hoverColor};

    ${Icon} {
      color: ${(props) => props.theme.sidebar.hoverColor};
    }
  }
`;

const NestedList = styled.ul`
  display: flex;
  flex-direction: column;
  position: absolute;
  top: 5rem;
  left: 2rem;
  list-style-type: none;
  padding: 0.5rem 1rem;
  border-radius: 10px;
  background-color: ${(props) => props.theme.sidebar.backgroundColor};
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
  ${ListItem} {
    margin: 0.5rem 0.25rem;
    padding: 0.5rem 1rem;
  }
`;

const ThemeChanger = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  margin: 1rem;
  padding: 0.3rem;
  cursor: pointer;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
  background-color: ${(props) => props.theme.sidebar.themeSwitcherBackground};
  align-self: center;
  width: fit-content;
  svg {
    color: ${(props) => props.theme.color};
  }
`;

const Expander = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  position: absolute;
  right: -0.8rem;
  top: 3.5rem;
  cursor: pointer;
  border-radius: 50%;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
  background-color: ${(props) => props.theme.sidebar.themeSwitcherBackground};
  ${Icon} {
    margin: 0.2rem;
  }
`;

const Header = styled.div`
  display: flex;
  align-items: flex-start;
  margin: 2rem;
  cursor: pointer;

  img {
    height: 40px;
  }
`;

const Subtitle = styled.p`
  color: #d7d5dd;
  text-transform: uppercase;
  font-size: 0.85rem;
  align-self: flex-start;
  margin: 1rem;
`;

const Divider = styled.div`
  height: 1px;
  width: 85%;
  background: #ddd;
  margin: 0 auto;
`;

//================================================

type SidebarProp = {
  options?: SidebarOption[];
  selectedOption?: Number;
  onOptionChange?: (index: Number) => void;
  companyID?: string;
};

function Sidebar(props: SidebarProp) {
  const [theme, setTheme] = useState("light");

  let navigate = useNavigate();

  const navigationHandler = (option: SidebarOption, index: number) => {
    if (props.onOptionChange) props.onOptionChange(index);
    navigate(`/companies/${props.companyID}/${option.link}`);
  };

  return (
    <Container>
      <Header onClick={() => (window.location.pathname = "/")}>
        <img src="/logo.svg" />
      </Header>

      <List>
        <Subtitle>Views</Subtitle>
        {navbarOptions.map((item, index) => (
          <ListItem
            key={index}
            onClick={() => (window.location.pathname = `${item.toLowerCase()}`)}
            active={window.location.pathname === `/${item.toLowerCase()}`}
          >
            {item}
          </ListItem>
        ))}
      </List>

      <Divider></Divider>

      {window.location.pathname.split("/")[1] === "companies" && (
        <List>
          <Subtitle>Options</Subtitle>
          {props?.options?.map((option, index) => {
            return (
              <ListItem onClick={() => navigationHandler(option, index)} active={index === props.selectedOption}>
                <Icon src={`/${option.icon}.svg`} /> {option.name}
              </ListItem>
            );
          })}
        </List>
      )}
    </Container>
  );
}

export default Sidebar;
