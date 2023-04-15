export const formatNumber = (value: number) => {
  const converted = new Intl.NumberFormat("en-US", {
    notation: "compact",
    maximumFractionDigits: 3
  }).format(value);

  return converted;
};

export const formatDate = (value: string) => {
  const options: Intl.DateTimeFormatOptions = { year: "2-digit", month: "short" };
  return new Date(value).toLocaleDateString(undefined, options);
};
