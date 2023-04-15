import styled from "styled-components";
import { sizeAndDown } from "../styles/responsive";

const StyledTestimonials = styled.div`
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin: 5rem auto;
`;

const Heading = styled.h1`
  color: #fdb44b;
  font-size: 3.5rem;
`;

const Card = styled.div`
  width: 25%;
  display: inline-flex;
  flex-direction: column;
  align-items: center;
  margin: 5rem 2rem;
  padding: 1.5rem 2rem;
  background-color: #f0f8fe;
  border-radius: 10px;

  ${sizeAndDown("lg")} {
    width: 60%;
    margin: 4rem auto;
  }
`;

const TestimonialText = styled.div`
  display: flex;
  flex-direction: column;
  font-size: 1.2rem;
  text-align: center;
  margin-bottom: auto;

  p {
    padding: 0 1.5rem;
  }
`;

const Open = styled.img`
  width: 2rem;
  align-self: flex-start;
`;

const Close = styled.img`
  width: 2rem;
  align-self: flex-end;
`;

const TestimonialImage = styled.img`
  width: 5rem;
  border-radius: 50%;
  margin: 4rem 0 2rem 0;
`;

const TestimonialName = styled.div`
  font-weight: 700;
  font-size: 1.2rem;
`;

const TestimonialDesignation = styled.div`
  font-size: 1.2rem;
`;

const TestimonialList = styled.div`
  display: flex;
  align-items: stretch;
  justify-content: center;

  ${sizeAndDown("md")} {
    flex-direction: column;
  }
`;

type TestimonialData = {
  name: string;
  designation: string;
  testimonial: string;
  image: string;
};

const SampleData: TestimonialData[] = [
  {
    name: "Abhijit Das",
    designation: "Professor",
    testimonial:
      "As a researcher, SaaSifi makes your life so easy! It is easy to navigate and provides everything I could ask from a SEC filing. Kudos to the team and highly recommended. ",
    image: "/abhijit_das.jpg"
  },
  {
    name: "Krishnam Kapoor",
    designation: "Quantitative Strategist, Quadeye Securities",
    testimonial:
      "To simply put it across, SaaSifi is love. By far, it is the tool with the greatest level of detail and insights into SEC filings. The feature to extract files in csv format is a huge add on, for us analysts. I also see that the tool updates itself with each filing which makes it fit for permanent use.",
    image: "/krishnam.jpg"
  },
  {
    name: "Vikrant Gupta",
    designation: "Equity Researcher, Alliance Bernstein",
    testimonial:
      "The team has focused on building a detail oriented web tool with requisite ease of use. I love the fact that the tool has a backtracking feature to see where the metrics came from. After seeing SaaSifi, i feel that the need to read SEC reports for SaaS is near to none. I wish the team all the best, way to go! ",
    image: "/vikrant.jpg"
  }
];

const TestimonialCard = (props: TestimonialData) => {
  return (
    <Card>
      <TestimonialText>
        <Open src="/open.svg"></Open>
        <p>{props.testimonial}</p>
        <Close src="/close.svg"></Close>
      </TestimonialText>
      <TestimonialImage src={props.image}></TestimonialImage>
      <TestimonialName>{props.name}</TestimonialName>
      <TestimonialDesignation>{props.designation}</TestimonialDesignation>
    </Card>
  );
};

export default function Testimonials() {
  return (
    <StyledTestimonials>
      <Heading>Testimonials</Heading>
      <TestimonialList>
        {SampleData.map((data) => {
          return <TestimonialCard {...data} />;
        })}
      </TestimonialList>
    </StyledTestimonials>
  );
}
