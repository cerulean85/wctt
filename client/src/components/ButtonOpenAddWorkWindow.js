import React from "react";
import * as R from "../Resources";

class ButtonOpenAddWorkWindow extends React.Component {

    constructor(props) {
        super(props);
        this.handleMouseHover = this.handleMouseHover.bind(this);
        this.handleMouseLeave = this.handleMouseLeave.bind(this);
        this.state = {
            backgroundColor: '#1b1b1b',
            opacity: 1.0,
        };
    }

    handleMouseHover() { this.setState(this.toggleHoverState); }
    handleMouseLeave() { this.setState(this.toggleLeaveState); }

    toggleHoverState(state) { return { backgroundColor: '#323232' }; }
    toggleLeaveState(state) { return { backgroundColor: '#1b1b1b' }; }

    update() {
        const expression = R.StateExpression[this.props.value];
        this.expression.label = expression.label;
        this.expression.backgroundColor = expression.backgroundColor;
    }

    render() {

        return (
            <div
                onMouseEnter={this.handleMouseHover}
                onMouseLeave={this.handleMouseLeave}
                onClick={() => this.props.onClick()}
                style={{
                    position: 'relative',
                    // opacity: this.state.opacity,
                    backgroundColor: this.state.backgroundColor,
                    cursor: 'pointer',
                    width: 150,
                    height: 80}}>
                <div style={{
                    display: 'flex',
                    position: 'absolute',
                    top: '53%',
                    left: '50%',
                    transform: 'translate(-50%, -50%)' }}>
                    <img src={R.Images.addWork}
                         style={{ width:20, height: 20, }} />
                    <div style={{
                        fontWeight:'bolder',
                        fontSize: 12,
                        color: '#ACACAC' }}>&nbsp;&nbsp;작업 추가</div>
                </div>
            </div>
        );
    }
}


export default ButtonOpenAddWorkWindow;