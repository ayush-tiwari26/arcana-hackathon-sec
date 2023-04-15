import { useTable } from "react-table";
import { TableProps } from "../types/table";
import styled from "styled-components";
import { MDAData } from "../types/company";

const Styles = styled.div`
  width: 100%;
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

const TableComponent = (props: any) => {
  const data = props.data;
  const columns = props.columns;

  const tableInstance = useTable({ columns, data });

  const { getTableProps, getTableBodyProps, headerGroups, rows, prepareRow } = tableInstance;

  return (
    <Styles>
      <table {...getTableProps()} cellPadding="0" cellSpacing="0">
        <thead>
          {
            // Loop over the header rows
            headerGroups.map((headerGroup) => (
              // Apply the header row props
              <tr {...headerGroup.getHeaderGroupProps()}>
                {
                  // Loop over the headers in each row
                  headerGroup.headers.map((column) => (
                    // Apply the header cell props
                    <th {...column.getHeaderProps()}>
                      {
                        // Render the header
                        column.render("Header")
                      }
                    </th>
                  ))
                }
              </tr>
            ))
          }
        </thead>
        {/* Apply the table body props */}
        <tbody {...getTableBodyProps()}>
          {
            // Loop over the table rows
            rows.map((row) => {
              // Prepare the row for display
              prepareRow(row);
              return (
                // Apply the row props
                <tr {...row.getRowProps()}>
                  {
                    // Loop over the rows cells
                    row.cells.map((cell) => {
                      // Apply the cell props
                      return (
                        <td {...cell.getCellProps()}>
                          {
                            // Render the cell contents
                            cell.render("Cell")
                          }
                        </td>
                      );
                    })
                  }
                </tr>
              );
            })
          }
        </tbody>
      </table>
    </Styles>
  );
};

export default TableComponent;
