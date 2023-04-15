import { Link } from "react-router-dom";
import styled from "styled-components";
import { sizeAndDown } from "../styles/responsive";

const Container = styled.div`
  width: 100%;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #eef8ff;

  ${sizeAndDown("md")} {
    flex-direction: column;
  }
`;

const SubContainer = styled.div`
  display: flex;
  flex-direction: column;
  max-width: 30%;

  ${sizeAndDown("md")} {
    margin: 2rem;
    max-width: none;
  }
`;

const Title = styled.div`
  font-size: 3rem;
  font-weight: bold;
  color: #000;
  margin: 2rem 0;
`;

const SubTitle = styled.div`
  font-size: 1.2rem;
  color: #666;
  margin: 1rem 0;
`;

const Image = styled.img`
  width: 50%;
  margin-left: 2rem;
  filter: drop-shadow(10px 10px 5px rgba(#000, 0.2));

  ${sizeAndDown("md")} {
    width: 100%;
    margin-left: 0;
  }
`;

const Button = styled.button`
  background-color: #fdb44b;
  color: #fff;
  font-size: 1.3rem;
  font-weight: 700;
  margin: 2rem 0;
  padding: 0.8rem 2.8rem;
  outline: none;
  border: none;
  border-radius: 10px;
  text-decoration: none;
    color: #383c41;
  width:100%;
  cursor:pointer;
 
`;

export default function Hero() {
  return (
    <Container>
      <SubContainer>
        <Title>Visualize what matters the most </Title>
        <SubTitle>
          Leave the hassle of reading hundreds of SEC filings to us & uncover the hidden SaaS metrics deep in these
          reports.
        </SubTitle>
       
          <Link to="/companies"> <Button>Go to dashboard</Button></Link>
        
      </SubContainer>

      <Image src="hero.svg" />
    </Container>
  );
}
