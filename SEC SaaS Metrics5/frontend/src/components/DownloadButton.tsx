import { CSVLink } from "react-csv";
import styled from "styled-components";
import { Download } from "react-feather";
import { FloatingButton } from "../styles/button";
import { OwnershipData, SpreadsheetData } from "../types/company";

const Icon = styled.svg`
  margin: 0.5rem;
  color: #333;
`;

type DownloadButtonProps = {
  fileName: string;
  data: SpreadsheetData[] | OwnershipData[];
};

export default function DownloadButton(props: DownloadButtonProps) {
  return (
    <CSVLink data={props.data} filename={props.fileName}>
      <FloatingButton>
        <Icon as={Download} />
        <p>Download sheet as csv!</p>
      </FloatingButton>
    </CSVLink>
  );
}
