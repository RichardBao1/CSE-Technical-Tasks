import { SetStateAction, Dispatch, FormEvent } from "react";
import { TableContents } from "../Table/Table";

interface AlertModalProps {
  useContents: Dispatch<SetStateAction<TableContents>>,
}

export default function AlertModal({useContents}: AlertModalProps) {
  function onSubmitEvent(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    // console.log((e.target as any)[0].value);

    const val = (e.target as any).elements[0].value
    if (val === '') {
      return;
    } 

    useContents( 
      prevTable => {
      return {
        ...prevTable, 
        rowContents: [
          ...prevTable.rowContents,
          {
            alert: val,
            status: '',
            updates: []
          }
      ]}
    })

    }
  
  

  
  return (
    <form data-testid='form' onSubmit={onSubmitEvent}>
      <label> Add new alert: </label>
      <input type='text' id='alert' name='alert' />
      <button type='submit'> Add </button>
    </form>
  )
}
