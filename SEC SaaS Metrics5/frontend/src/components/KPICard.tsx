import { ChevronDown, ChevronUp, MoreHorizontal } from "react-feather";
import styled from "styled-components";
import { KPICardDetail } from "../types/company";
import { formatNumber } from "../utils/helpers";

const Card = styled.div`
  display: inline-flex;
  flex-direction: column;
  align-items: center;
  background-color: #fff;

  margin: 1rem;
  padding: 1rem;
  border-radius: 10px;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
`;

const Icon = styled.svg`
  stroke-width: 4px;
`;

const HorizontalContainer = styled.div`
  width: 100%;
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  text-align: center;
  padding: 1rem;
`;

const HeaderText = styled.div`
  font-weight: 700;
`;

const MainText = styled.div`
  font-size: 3rem;
  margin: 1rem 0;
  color: #184e77;
`;

const FooterText = styled.div`
  font-size: 1rem;
`;

export default function KPICard(props: KPICardDetail) {
  const percentChange: number = props.isPrevAvailable ? ((props.value - props.valuePrev) / props.valuePrev) * 100 : 0;
  const prefix = "Multiple on IPO Price";
  const prefix_2 = "Share price";
  const prefix_3 = "Percent of 52 week high";
  const prefix_4 = "EV";
  const prefix_5 = "EV/LTM Revenue";
  const prefix_6 = "EV/Revenue Run rate";
  return (
    <Card>
      <HorizontalContainer>
        <HeaderText>{props.name}</HeaderText>
        {/* <Icon as={MoreHorizontal} /> */}
      </HorizontalContainer>
      {prefix === props.name ? (
        <MainText>{formatNumber(props.value)}x</MainText>
      ) : prefix_3 === props.name ? (
        <MainText>{formatNumber(props.value * 100)}%</MainText>
      ) : (
        <MainText>$ {formatNumber(props.value)}</MainText>
      )}

      {props.isPrevAvailable ? (
        <HorizontalContainer>
          <FooterText>
            {prefix === props.name
              ? formatNumber(props.valuePrev) + "x vs last closing day"
              : prefix_2 === props.name
              ? formatNumber(props.valuePrev) + "$ vs last closing day"
              : prefix_4 === props.name || prefix_5 === props.name || prefix_6 === props.name
              ? formatNumber(props.valuePrev) + " vs last reported year "
              : "$" + formatNumber(props.valuePrev) + " vs previous period"}
          </FooterText>
          <FooterText>
            <Icon color={`${percentChange >= 0 ? "green" : "red"}`} as={percentChange >= 0 ? ChevronUp : ChevronDown} />
            <br /> {formatNumber(percentChange)}% change
          </FooterText>
        </HorizontalContainer>
      ) : null}
    </Card>
  );
}
