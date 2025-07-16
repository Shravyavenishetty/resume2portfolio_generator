import React from 'react';
import './styles.css';

const App = () => {
  return (
    <div className="container">
      <header>
        <h1>user@{{name}}:~$ whoami</h1>
        <p>{{summary}}</p>
      </header>
      <section>
        <h2>skills --list</h2>
        <p>{JSON.parse('{{skills}}').join(', ')}</p>
      </section>
      <section>
        <h2>education --history</h2>
        {JSON.parse('{{education}}').map((item, index) => (
          <p key={index}>{item}</p>
        ))}
      </section>
      <section>
        <h2>experience --log</h2>
        {JSON.parse('{{experience}}').map((item, index) => (
          <p key={index}>{item}</p>
        ))}
      </section>
      <section>
        <h2>projects --show</h2>
        {JSON.parse('{{projects}}').map((item, index) => (
          <p key={index}>{item}</p>
        ))}
      </section>
      <section>
        <h2>contact --info</h2>
        <p>{{contact}}</p>
      </section>
    </div>
  );
};

export default App;