import axios from "axios";
import { useEffect } from "react";
import styled from "styled-components";
import { Company, useSearchContext } from "../hooks/useSearchContext";
import { BACKEND_URL } from "../utils/constants";
import fuzzysort from "fuzzysort";
import { InputRow, Label, StyledInput } from "../styles/form";
import Select from "react-select";

const StyledSearch = styled.div`
  display: flex;
  align-items: flex-end;
  padding: 1.5rem 0;
  background-color: ${(props) => props.theme.sidebar.backgroundColor};
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.15);

  position: relative;
`;

const SearchInput = styled(StyledInput)`
  flex: 1;
  max-width: 20rem;
  width: 20rem;
`;

const Dropdown = styled.div`
  position: absolute;
  top: 7rem;
  cursor: pointer;

  padding: 0.75rem 1rem;
  background: #ffffff;
  border: 1px solid #efefef;
  box-sizing: border-box;
  border-radius: 8px;
  font-size: 1rem;
  max-width: 70%;
  margin: 0 0.5rem;
`;

const Icon = styled.svg`
  color: ${(props) => props.theme.sidebar.color};
  padding-left: 1rem;
`;

const filingTypes = [
  {
    value: "10-K",
    label: "10-K"
  },
  {
    value: "10-Q",
    label: "10-Q"
  },
  {
    value: "8-K",
    label: "8-K"
  }
];

const sources = [
  {
    value: "xbrl",
    label: "xbrl"
  },
  {
    value: "text",
    label: "text"
  }
];

const showFilingSelector = () => {
  const temp = window.location.pathname.split("/").filter((name) => name.length !== 0);
  if (temp.length === 0) return false;
  const path = temp[temp.length - 1];
  if (path === "spreadsheet") return true;
  return false;
};

export default function Search({ showFilters, showDropdown }: { showFilters: boolean; showDropdown: boolean }) {
  const {
    query,
    setQuery,
    results,
    companies,
    setCompanies,
    setResults,
    filters,
    setFilters,
    setSelectedCompanies,
    selectedFilings,
    setSelectedFilings,
    selectedSource,
    setSelectedSource
  } = useSearchContext();

  console.log(filingTypes);

  useEffect(() => {
    axios
      .get(`${BACKEND_URL}/companies_list`)
      .then((response) => {
        const tempCompanyList: Company[] = [];

        for (var i = 0; i < Object.keys(response.data).length; i++) {
          tempCompanyList.push({
            name: Object.keys(response.data)[i],
            // @ts-ignore
            id: Object.values(response.data)[i]
          });
        }

        setCompanies(tempCompanyList);
      })
      .catch((error) => {
        console.log(error);
      });
  }, []);

  useEffect(() => {
    if (query !== "") {
      setResults(fuzzysort.go(query, companies, { key: "name" }).map((item) => item.obj));
    } else {
      setResults(companies);
    }
  }, [companies, query]);

  return (
    <StyledSearch>
      {!showDropdown ? (
        <InputRow>
          <Label>Search</Label>
          <SearchInput
            style={{ minWidth: "500px" }}
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="Search companies"
          />
          {query !== "" && (
            <Dropdown>
              {results.slice(0, 10).map((item) => (
                <p onClick={() => (window.location.pathname = `/companies/${item.id}`)}>{item.name}</p>
              ))}
            </Dropdown>
          )}
        </InputRow>
      ) : (
        <InputRow>
          <Label>Select Company</Label>
          <Select
            className="basic-single"
            isMulti={true}
            classNamePrefix="select"
            options={companies.map((item) => ({ value: item.id, label: item.name }))}
            onChange={(options) => {
              console.log("options", options);
              setSelectedCompanies(options.map((item) => ({ id: item.value, name: item.label })));
            }}
          />
        </InputRow>
      )}

      {showFilters && (
        <>
          <InputRow>
            <Label>Date Range</Label>
            <div>
              <StyledInput
                type="date"
                placeholder="From"
                value={filters.startDate}
                onChange={(e) => setFilters({ startDate: e.target.value, endDate: filters.endDate })}
              />
              <StyledInput
                type="date"
                placeholder="To"
                value={filters.endDate}
                onChange={(e) => setFilters({ startDate: filters.startDate, endDate: e.target.value })}
              />
            </div>
          </InputRow>
        </>
      )}

      {showFilingSelector() && (
        <InputRow>
          <Label>Filing types</Label>
          <Select
            className="basic-single"
            isMulti={true}
            classNamePrefix="select"
            options={filingTypes}
            value={selectedFilings}
            onChange={(options) => {
              console.log("options", options);
              setSelectedFilings(options.map((item) => item));
            }}
          />
        </InputRow>
      )}

      {showFilingSelector() && (
        <InputRow>
          <Label>Source</Label>
          <Select
            className="basic-single"
            isMulti={true}
            classNamePrefix="select"
            options={sources}
            value={selectedSource}
            onChange={(options) => {
              setSelectedSource(options.map((item) => item));
            }}
          />
        </InputRow>
      )}
    </StyledSearch>
  );
}
