import { css } from "styled-components";

export const breakpoints = {
  xs: "480px",
  sm: "768px",
  md: "992px",
  lg: "1200px"
};

export const breakpoints_exclusive = {
  xs: ["0px", "480px"],
  sm: ["481px", "768px"],
  md: ["767px", "992px"],
  lg: ["993px", "1200px"],
  xl: ["1201px", "100000px"]
};

export const sizeAndUp = (key: keyof typeof breakpoints) => {
  return () => `@media (min-width: ${breakpoints[key]})`;
};

export const sizeAndDown = (key: keyof typeof breakpoints) => {
  return () => `@media (max-width: ${breakpoints[key]})`;
};

export const sizeExclusive = (key: keyof typeof breakpoints) => {
  return (style: TemplateStringsArray | String) =>
    `@media (min-width: ${breakpoints_exclusive[key][0]}) and (min-width: ${breakpoints_exclusive[key][1]})`;
};
