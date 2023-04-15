import { NavLink } from "react-router-dom";
import styled from "styled-components";
import { sizeAndDown } from "../styles/responsive";
import { Menu, X } from "react-feather";
import { useState } from "react";
import { navbarOptions } from "../utils/constants";

const Wrapper = styled.div`
  height: auto;
  width: 100%;
`;

const Open = styled.img`
  width: 8rem;
  align-self: flex-start;
`;

const Container = styled.div<{ active: boolean }>`
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  width: 100%;
  background-color: #90e0ef;
  padding: 0 3rem;

  ${sizeAndDown("md")} {
    display: ${(props) => (props.active ? "flex" : "none")};
    padding: 0;
    position: fixed;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100vh;
  }
`;

const Icon = styled.svg`
  align-items: flex-end;
  color: #333;
  position: fixed;
  top: 1rem;
  right: 2rem;
  display: none;
  z-index: 99;

  ${sizeAndDown("md")} {
    display: block;
  }
`;

const ListView = styled.div`
  cursor: pointer;
  margin: 1.8rem 1.2rem;

  padding: 0.8rem 1.2rem;
  a {
    text-decoration: none;
    border-radius: 10px;
    color: #383c41;
    padding: 1rem;

    &:hover {
      background-color: #3bc8e2;
    }
  }

  ${sizeAndDown("md")} {
    margin: 0;

    a {
      margin: 1.8rem 1.2rem;
    }
  }
`;

const LogoView = styled.div`
  cursor: pointer;

  a {
    text-decoration: none;
    padding: 1rem 1rem;
    border-radius: 10px;
    color: ${(props) => props.theme.sidebar.hoverColor};
    font-weight: 700;
    font-size: 1.5rem;
  }

  ${sizeAndDown("md")} {
    display: none;
  }
`;

export default function Navbar() {
  const [expandMenu, setExpandMenu] = useState<boolean>(false);

  return (
    <Wrapper>
      <Icon as={expandMenu ? X : Menu} onClick={() => setExpandMenu(!expandMenu)} />

      <Container active={expandMenu}>
        <LogoView>
          <NavLink to="/">
            <Open src="/logo.svg"></Open>
          </NavLink>
        </LogoView>
        {navbarOptions.map((option) => {
          return (
            <ListView>
              <NavLink to={`/${option.toLowerCase()}`}>{option}</NavLink>
            </ListView>
          );
        })}
      </Container>
    </Wrapper>
  );
}
