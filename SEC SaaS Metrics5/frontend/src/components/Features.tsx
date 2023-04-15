import styled from "styled-components";
import { sizeAndDown } from "../styles/responsive";

interface Step {
  title: string;
  description: string;
  illustration: string;
}

const steps: Step[] = [
  {
    title: "Customizability",
    description:
      "Create Personalised dashboards with metrics and visuals of your choice and track your favourite firms",
    illustration: "/sustomisability.svg"
  },
  {
    title: "Deep Insights",
    description: "Understand the ins and outs of SaaS with insightful and accurate metrics",
    illustration: "/insights.svg"
  },
  {
    title: "Ease of Use",
    description: "Feel the ease of usability along with a host of different slice and dice features",
    illustration: "/ease.svg"
  }
];

const StyledFeatures = styled.div`
  width: 90%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin: 5rem auto;

  ${sizeAndDown("md")} {
    width: 80%;
  }
`;
const Title = styled.h3`
  font-size: 2.1rem;
`;
const Description = styled.p`
  font-size: 1.3rem;
`;
const Heading = styled.h1`
  color: #fdb44b;
  font-size: 3.5rem;
  margin: 0 1rem;
`;
const FeatureImg = styled.img`
  ${sizeAndDown("lg")} {
    width: 40%;

    img {
      width: 100%;
    }

    div {
      font-size: 1.2rem;
      width: 100%;
      padding: 0 1.5rem;
    }
  }
`;
const Card = styled.div`
  width: 100%;
  display: flex;
  justify-content: space-evenly;
  align-items: center;
  margin: 5rem 1rem;

  div {
    width: 30%;
    font-size: 1.5rem;
  }

  &:nth-of-type(even) {
    flex-direction: row-reverse;
  }

  img {
    width: 40%;
  }

  ${sizeAndDown("md")} {
    margin: 1rem 0;
    display: block;

    img {
      width: 80%;
      padding: 0 1.5rem;
    }

    div {
      font-size: 1.2rem;
      width: 80%;
      padding: 0 1.5rem;
    }
  }
`;

const CardContainer = styled.div`
  width: 100%;
  display: flex;
  flex-direction: column;
`;

export default function Features() {
  return (
    <StyledFeatures>
      <Heading>Features</Heading>
      <CardContainer>
        {steps.map((item) => (
          <Card>
            <div>
              <Title>
                <h3>{item.title}</h3>
              </Title>
              <Description>
                <p>{item.description}</p>
              </Description>
            </div>
            <FeatureImg src={item.illustration}></FeatureImg>
          </Card>
        ))}
      </CardContainer>
    </StyledFeatures>
  );
}
