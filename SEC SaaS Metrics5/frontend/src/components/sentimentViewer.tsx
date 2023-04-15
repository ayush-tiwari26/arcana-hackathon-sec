import { X } from "react-feather";
import styled from "styled-components";

const Wrapper = styled.div`
  width: 100%;
  min-height: 100vh;
  position: fixed;
  top: 0;
  left: 0;
  backdrop-filter: blur(5px);
`;

const Viewer = styled.div`
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 100;
  width: 70%;
  height: 70vh;
  overflow-y: scroll;
  background-color: #d5eeff;
  padding: 4rem 5rem;
  border-radius: 10px;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
`;

const Icon = styled.svg`
  margin: 0.5rem;
  color: #333;
  position: fixed;
  top: 1rem;
  left: 1rem;
`;

export default function SentimentViewer(props: any) {
  const insertHighlight = (text: string) => {
    const highlights: any[] = [];
    for (var i = 0; i < props.data.positive.length; i++) {
      highlights.push({
        range: props.data.positive[i],
        type: "positive"
      });
    }
    for (var i = 0; i < props.data.negative.length; i++) {
      highlights.push({
        range: props.data.negative[i],
        type: "negative"
      });
    }

    highlights.sort((a, b) => {
      return a.range[0] - b.range[0];
    });

    var offset = 0;

    for (var i = 0; i < highlights.length; i++) {
      if (highlights[i].type === "positive") {
        text =
          text.slice(0, highlights[i].range[0] + offset) +
          "<span style='color: green;'>" +
          text.slice(highlights[i].range[0] + offset);
        offset += 28;
      } else {
        text =
          text.slice(0, highlights[i].range[0] + offset) +
          "<span style='color: red;'>" +
          text.slice(highlights[i].range[0] + offset);
        offset += 26;
      }
      text = text.slice(0, highlights[i].range[1] + offset) + "</span>" + text.slice(highlights[i].range[1] + offset);
      offset += 7;
    }

    return text;
  };

  return (
    <Wrapper>
      <Viewer>
        <Icon size={30} onClick={() => props.close()} as={X} />
        <div dangerouslySetInnerHTML={{ __html: insertHighlight(props.data.text) }}></div>
      </Viewer>
    </Wrapper>
  );
}
