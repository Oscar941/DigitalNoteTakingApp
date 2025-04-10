import React, { useState, useEffect } from 'react';
import axios from 'axios';

// Example: A simplified global cache to avoid refetching data
const globalCache = {};

function NoteList() {
    const [notes, setNotes] = useState([]);

    useEffect(() => {
        const fetchNotes = async () => {
            const cacheKey = 'notes';
            if (globalCache[cacheKey]) {
              setNotes(globalCache[cacheKey]);
              return;
            }
            
            try {
                const response = await axios.get('https://your.api/notes');
                globalCache[cacheKey] = response.data;
                setNotes(response.data);
            } catch (error) {
                console.error("Failed to fetch notes:", error);
            }
        };

        fetchNotes();
    }, []);

    return (
      <div>
        {notes.map(note => (
          <div key={note.id}>{note.title}</div>
        ))}
      </div>
    );
}