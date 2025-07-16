import React from 'react';
import './styles.css';

const App = () => {
  return (
    <div className="container">
      <header>
        <h1>{{name}}</h1>
        <p>{{summary}}</p>
      </header>
      <section>
        <h2>Skills</h2>
        <p>{JSON.parse('{{skills}}').join(', ')}</p>
      </section>
      <section>
        <h2>Education</h2>
        {JSON.parse('{{education}}').map((item, index) => (
          <p key={index}>{item}</p>
        ))}
      </section>
      <section>
        <h2>Experience</h2>
        {JSON.parse('{{experience}}').map((item, index) => (
          <p key={index}>{item}</p>
        ))}
      </section>
      <section>
        <h2>Projects</h2>
        {JSON.parse('{{projects}}').map((item, index) => (
          <p key={index}>{item}</p>
        ))}
      </section>
      <section>
        <h2>Contact</h2>
        <p>{{contact}}</p>
      </section>
    </div>
  );
};

export default App;