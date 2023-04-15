import { Route, Routes } from "react-router-dom";
import Benchmarking from "./views/Benchmarking";
import CompanyPage from "./views/CompanyPage";
import Dashboard from "./views/Dashboard";
import MainArea from "./views/MainArea";

export default function Switch() {
  return (
    <Routes>
      <Route path="/" element={<MainArea />} />
      <Route path="/companies" element={<CompanyPage />} />
      <Route path="/companies/:id/*" element={<CompanyPage />} />
      <Route path="/benchmarking" element={<Benchmarking />} />
    </Routes>
  );
}
