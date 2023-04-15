import axios from "axios";
import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import Select from "react-select";
import styled from "styled-components";
import { Finance } from "../types/company";
import { BACKEND_URL } from "../utils/constants";

type option = {
  value: string;
  label: string;
};

const Container = styled.div`
  width: 100%;
  h2 {
    text-align: center;
    margin-top: 5rem;
  }
`;

const SelectList = styled.div`
  display: flex;
  margin: 1rem 0 2rem 2rem;
  width: 40rem;
  justify-content: space-evenly;
`;

const Table = styled.div`
  table {
    width: 90%;
    background-color: ${(props) => props.theme.sidebar.backgroundColor};
    border-radius: 10px;

    overflow: hidden;
    margin: 1rem auto;

    text-align: left;
    tr {
      td {
        padding: 0.5rem 1rem;
        border: 1px solid #ddd;
      }
      &:nth-of-type(even) {
        background-color: ${(props) => props.theme.sidebar.hoverBackground};
      }
    }

    th {
      background-color: ${(props) => props.theme.sidebar.themeSwitcherBackground};
      color: ${(props) => props.theme.table.headerColor};
      fontweight: bold;
      padding: 0.4rem 1rem;
    }
  }
`;

export default function CompanyFinance() {
  const [financeData, setFinanceData] = useState<Finance>([]);
  const [years, setYears] = useState<option[]>([]);
  const [selectedYear, setSelectedYear] = useState<number>(-1);
  const [sheets, setSheets] = useState<option[]>([]);
  const [selectedSheet, setSelectedSheet] = useState<number>(-1);
  const [tableHTML, setTableHTML] = useState<string>("<h2>Loading...</h2>");

  let params = useParams();

  const getOptionIndex = (options: option[], selectedOption: option | null) => {
    if (selectedOption === null) return -1;
    for (var i = 0; i < options.length; i++) {
      if (options[i].value === selectedOption.value) return i;
    }
    return -1;
  };

  useEffect(() => {
    axios
      .get(`${BACKEND_URL}/read_html?cik=${params.id}`)
      .then((response) => setFinanceData(response.data))
      .catch((error) => console.log(error));
  }, []);

  useEffect(() => {
    const temp: option[] = [];
    financeData.map((data) => {
      temp.push({
        label: data.year,
        value: data.year
      });
    });
    setYears(temp);
    if (temp.length > 0) setSelectedYear(0);
    else setSelectedYear(-1);
  }, [financeData]);

  useEffect(() => {
    if (selectedYear !== -1) {
      const temp: option[] = [];
      financeData[selectedYear].data.map((tableData) => {
        temp.push({
          label: tableData.tablename,
          value: tableData.tablename
        });
      });
      setSheets(temp);
      if (temp.length > 0) setSelectedSheet(0);
      else setSelectedSheet(-1);
    } else setSelectedSheet(-1);
  }, [selectedYear]);

  useEffect(() => {
    if (selectedSheet !== -1) {
      setTableHTML(financeData[selectedYear].data[selectedSheet].table_data);
    } else setTableHTML("<h2>Loading...</h2>");
  }, [selectedYear, selectedSheet]);

  return (
    <Container>
      <SelectList>
        <Select
          options={years}
          value={years[selectedYear]}
          onChange={(value) => setSelectedYear(getOptionIndex(years, value))}
        />
        <Select
          options={sheets}
          value={sheets[selectedSheet]}
          onChange={(value) => setSelectedSheet(getOptionIndex(sheets, value))}
        />
      </SelectList>
      <Table dangerouslySetInnerHTML={{ __html: tableHTML }}></Table>
    </Container>
  );
}
