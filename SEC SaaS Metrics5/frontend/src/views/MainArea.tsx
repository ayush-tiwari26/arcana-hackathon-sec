import styled from "styled-components";
import Footer from "../components/Footer";
import Hero from "../components/Hero";
import Features from "../components/Features";
import Testimonials from "../components/Testimonials";
import Navbar from "../components/Navbar";

const Container = styled.div`
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: #ffffff;
`;

export default function MainArea() {
  return (
    <Container>
      <Navbar />
      <Hero />
      <Features />
      <Testimonials />
      <Footer />
    </Container>
  );
}
