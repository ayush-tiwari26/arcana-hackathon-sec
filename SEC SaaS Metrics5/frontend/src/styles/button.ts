import styled from "styled-components";

export const FloatingButton = styled.div`
  position: fixed;
  right: 2rem;
  bottom: 1rem;
  z-index: 10;
  background-color: #d5eeff;
  padding: 1rem;
  border-radius: 50%;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);

  p {
    display: none;
    color: #333;
  }

  &:hover {
    display: flex;
    align-items: center;
    border-radius: 1rem;
    padding: 0.5rem 1rem;
    p {
      display: block;
    }
  }
`;

export const Button = styled.div`
  cursor: pointer;
  background: #ffffff;
  padding: 0.75rem 1rem;
  border: 1px solid #efefef;
  box-sizing: border-box;
  border-radius: 8px;
  font-size: 1rem;
  display: inline-flex;
  align-items: center;
`;
