import React, { createContext, useContext, useState } from "react";

export type Company = {
  name: string;
  id: string;
};

export type Filters = {
  startDate: string;
  endDate: string;
};

type SearchContextType = {
  query: string;
  setQuery: (val: string) => void;
  filters: Filters;
  setFilters: (val: Filters) => void;
  companies: Company[];
  setCompanies: (val: Company[]) => void;
  selectedCompanies: Company[];
  setSelectedCompanies: (val: Company[]) => void;
  results: Company[];
  setResults: (val: Company[]) => void;
  isQueryEmpty: () => boolean;
  selectedFilings: any[];
  setSelectedFilings: (val: any[]) => void;
  selectedSource: any[];
  setSelectedSource: (val: any[]) => void;
  // TODO: other form inputs and filters would go here
};

const SearchContext = createContext<SearchContextType>(undefined!);
export const useSearchContext = () => useContext(SearchContext);

export const SearchProvider: React.FC = ({ children }: any) => {
  const [query, setQuery] = useState("");
  const [companies, setCompanies] = useState<Company[]>([{ name: "", id: "" }]);
  const [selectedCompanies, setSelectedCompanies] = useState<Company[]>([]);
  const [results, setResults] = useState<Company[]>([{ name: "", id: "" }]);
  // TODO: make these initial values better
  const [filters, setFilters] = useState<Filters>({ startDate: "2015-01-01", endDate: "2023-01-01" });
  const [selectedFilings, setSelectedFilings] = useState<any[]>([
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
  ]);
  const [selectedSource, setSelectedSource] = useState<any[]>([
    {
      value: "xbrl",
      label: "xbrl"
    },
    {
      value: "text",
      label: "text"
    }
  ]);

  const isQueryEmpty = () => {
    return query === null || query === undefined || query.trim().length === 0;
  };

  const value = {
    query,
    setQuery,
    companies,
    setCompanies,
    selectedCompanies,
    setSelectedCompanies,
    results,
    setResults,
    filters,
    setFilters,
    isQueryEmpty,
    selectedFilings,
    setSelectedFilings,
    selectedSource,
    setSelectedSource
  };

  return <SearchContext.Provider value={value}>{children}</SearchContext.Provider>;
};
