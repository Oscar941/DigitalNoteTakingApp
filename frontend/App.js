import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import NoteList from './NoteList';
import NoteDetail from './NoteDetail';
import CreateNote from './CreateNote';
import NotebookList from './NotebookList';

function App() {
  return (
    <Router>
      <div>
        <Switch>
          <Route path="/noteList" exact component={NoteList} />
          <Route path="/noteDetail/:id" component={NoteDetail} />
          <Route path="/createNote" component={CreateNote} />
          <Route path="/notebookList" component={NotebookList} />
          <Route path="/" exact component={NoteList} />
        </Switch>
      </div>
    </Router>
  );
}

export default App;