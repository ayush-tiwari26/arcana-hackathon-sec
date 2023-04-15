import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import styled from "styled-components";
import axios from "axios";
import { BACKEND_URL } from "../utils/constants";
import KPICard from "./KPICard";
import { KPICardDetail, Metadata } from "../types/company";
import CompanyCharts from "./CompanyCharts";

const Container = styled.div`
  display: flex;
  flex-direction: column;
  width: 100%;
  margin: 1rem;
`;

// TODO: when the colors are decided move and take them from the theme

const KPICardList = styled.div`
  display: block;
  margin-top: 4rem;
`;

const KPISpecialCardList = styled.div`
  display: flex;
  flex-wrap: wrap;
  max-width: 50%;
`;

const DescComponent = styled.div`
  width: 100%;
  display: flex;
`;

const DescContainer = styled.div`
  display: flex;
  flex-direction: column;
  margin-left: 1rem;
`;

const DescSubComponent = styled.div`
  display: flex;
  flex-direction: column;
  margin-left: 1rem;

  p {
    font-size: 1.25rem;
    max-width: 80ch;
  }
`;

const SubTitle = styled.div`
  font-size: 2rem;
  margin: 2rem 0 1rem 0;
  font-weight: bold;
`;

const TagList = styled.div`
  display: flex;
  flex-direction: column;
  align-items: stretch;
`;

const Tag = styled.div`
  width: 5rem;
  padding: 0.6rem 0.5rem;
  border-radius: 10px;
  background-color: #d5eeff;
`;

export default function CompanyMetadata(props: Metadata) {
  let params = useParams();

  const [desc, setDesc] = useState<String>("");
  const [categories, setCategories] = useState<String[]>([]);
  const [KPIList, setKPIList] = useState<KPICardDetail[]>([]);
  const [KPISpecialList, setKPISpecialList] = useState<KPICardDetail[]>([]);

  useEffect(() => {
    const companyMetadata: Metadata = props;
    setCategories([companyMetadata.category]);
    setDesc(companyMetadata.overview);
  }, [props]);

  useEffect(() => {
    axios
      .get(`${BACKEND_URL}/yahoo_finance?cik=${params.id}`)
      .then((response) => {
        const { tag, value, prevpresent, prevvalue } = response.data;
        const length = tag.length;
        const tempSpecial: KPICardDetail[] = [];
        const tempNormal: KPICardDetail[] = [];
        for (var i = 0; i < length; i++) {
          if (
            tag[i] === "Multiple on IPO Price" ||
            tag[i] === "Share price" ||
            tag[i] === "Percent of 52 week high" ||
            tag[i] === "Market Cap"
          ) {
            tempSpecial.push({
              name: tag[i],
              value: value[i],
              isPrevAvailable: prevpresent[i] === 1,
              valuePrev: prevvalue[i]
            });
          } else {
            tempNormal.push({
              name: tag[i],
              value: value[i],
              isPrevAvailable: prevpresent[i] === 1,
              valuePrev: prevvalue[i]
            });
          }
        }
        setKPISpecialList(tempSpecial);
        setKPIList(tempNormal);
      })
      .then((err) => console.log(err));
  }, []);

  return (
    <Container>
      <DescComponent>
        <KPISpecialCardList>
          {KPISpecialList.map((cardDetails) => {
            return <KPICard {...cardDetails} />;
          })}
        </KPISpecialCardList>

        <DescContainer>
          <DescSubComponent style={{ paddingRight: "5rem" }}>
            <SubTitle>Description</SubTitle>
            <p>{desc}</p>
          </DescSubComponent>

          <DescSubComponent>
            <SubTitle>CIK</SubTitle>
            <TagList>
              <Tag>{params.id}</Tag>
              {/* {categories.map((company) => {
                return <Tag>{company}</Tag>;
              })} */}
            </TagList>
          </DescSubComponent>
        </DescContainer>
      </DescComponent>

      <KPICardList>
        {KPIList.map((cardDetails) => {
          return <KPICard {...cardDetails} />;
        })}
      </KPICardList>

      <CompanyCharts />
    </Container>
  );
}
