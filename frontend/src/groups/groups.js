import React from "react";
import {apiBaseURL} from "../App";

export default class Groups extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            user: props.user,
            groups: []
        }
        this.onLeave = this.onLeave.bind(this);
    }

    componentDidMount() {
        let options = {
            headers: {
                'Content-Type': 'application/json'
            },
            method: "POST",
            body: JSON.stringify({user: this.state.user})
        }
        fetch(apiBaseURL + 'groups/mine', options)
            .then(resp => resp.json())
            .then(resp => this.setState({groups: resp.groups}),
                  err => console.log(err));
    }

    onLeave(e) {
        let target = e.target;
        let options = {
            headers: {
                'Content-Type': 'application/json'
            },
            method: "POST",
            body: JSON.stringify({user: this.state.user, id: target.name})
        }
        fetch(apiBaseURL + "groups/leave", options)
            .then(() => this.componentDidMount(),
                  err => console.log(err))
    }

    render() {
        return (
            <div>
                <h1>This is the groups page!</h1>
                {!this.state.groups && 
                    <div>
                        <h2>Here are your groups! Huzzah!</h2>
                        <ul>
                            {this.state.groups.map((group, index) => (
                                <li key={index}>{group.name}
                                <button name={group.id} onClick={this.onLeave}>Leave</button></li>))}
                        </ul>
                    </div>
                }
            </div>
        );
    }
}