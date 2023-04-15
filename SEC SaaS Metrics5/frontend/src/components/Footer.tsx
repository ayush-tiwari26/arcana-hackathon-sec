import styled from "styled-components";
import { sizeAndDown } from "../styles/responsive";

// TODO: colours from theme
const Container = styled.div`
  width: 100%;
  min-height: 10vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: #90e0ef;
  color: #333;
  font-size: 1.1rem;
`;
//

const SubContainer = styled.div`
  display: flex;
  justify-content: space-evenly;
  margin: 2rem 0;

  ${sizeAndDown("md")} {
    flex-direction: column;
  }
`;
const Open = styled.img`
  width: 25rem;
  align-self: flex-start;
  margin-top: 2rem;
  ${sizeAndDown("md")} {
    width: 80%;
  }
`;
// margin: 0 5rem 1rem 5rem;
const LargeColumn = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 0;

  h1 {
    font-size: 2.5rem;
  }

  div {
    font-size: 1.1rem;
    color: #555;
  }
`;

const SmallColumn = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 2rem 3rem 1rem 3rem;

  div {
    margin: 0.5rem 0;
  }
`;

export default function Footer() {
  return (
    <Container>
      <SubContainer>
        <LargeColumn>
          <Open src="/logo.svg"></Open>
        </LargeColumn>
        {/* <LargeColumn>
          <h1>Digital Alpha</h1>
          <div>Beautiful informative dashboards.</div>
        </LargeColumn> */}
        {/* TODO: map these and change to links */}
        {/* <SmallColumn>
          <div>Terms and Conditions</div>
          <div>Privacy Policy</div>
        </SmallColumn>
        <SmallColumn>
          <div>About Us</div>
          <div>Contact Us</div>
          <div>Blog</div>
        </SmallColumn>
        <SmallColumn>
          <div>Pricing</div>
          <div>Features</div>
        </SmallColumn> */}
      </SubContainer>
      <SubContainer>© 2022 SaaSiFi</SubContainer>
    </Container>
  );
}
