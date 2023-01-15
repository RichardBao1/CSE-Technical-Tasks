import { SetStateAction, Dispatch, FormEvent } from "react";
import { TableContents } from "../Table/Table";

interface AlertModalProps {
  useContents: Dispatch<SetStateAction<TableContents>>,
}

interface AlertModalProps {
  useContents: Dispatch<SetStateAction<TableContents>>,
}

interface AlertUpdate {
  date: string,
  update: string
}

interface Alert {
  alert: string,
  status: string,
  updates: AlertUpdate[]
}


export default function AlertModal({useContents}: AlertModalProps) {
  function onSubmitEvent(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    // hint: the alert given is at (e.target as any).elements[0].value - ignore typescript being annoying
    console.log((e.target as any)[0].value);

    const newContent: Alert = {
      alert: (e.target as any)[0].value,
      status: "Woah",
      updates: []
    }

    useContents(contents => {
      contents.rowContents.push(newContent);
      return contents;
    });


    }
  
  

  
  return (
    <form data-testid='form' onSubmit={onSubmitEvent}>
      <label> Add new alert: </label>
      <input type='text' id='alert' name='alert' />
      <button type='submit'> Add </button>
    </form>
  )
}
