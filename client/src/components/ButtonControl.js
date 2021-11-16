import React from "react";
import * as R from "../Resources";
import {ControlButtonStyle} from "../Resources";

class ButtonControl extends React.Component {

    constructor(props) {
        super(props);
        this.handleMouseHover = this.handleMouseHover.bind(this);
        this.handleMouseLeave = this.handleMouseLeave.bind(this);
        this.state = {
            opacity: 1.0,
        };
    }

    handleMouseHover() { this.setState(this.toggleHoverState); }
    handleMouseLeave() { this.setState(this.toggleLeaveState); }

    toggleHoverState(state) { return { opacity: 0.5 }; }
    toggleLeaveState(state) { return { opacity: 1.0 }; }

    update() {
        const expression = R.StateExpression[this.props.value];
        this.expression.label = expression.label;
        this.expression.backgroundColor = expression.backgroundColor;
    }

    componentDidUpdate(prevProps, prevState, snapshot) {

    }

    render() {
        let btnColor = R.ControlButtonStyle[this.props.value].bgColor
        let btnName = R.ControlButtonStyle[this.props.value].name
        return (
            <div
                style={
                    {
                        width: 80,
                        height: 40,
                        border: '0px',
                        position: 'relative',
                        opacity: this.state.opacity,
                        cursor: 'pointer',
                    }
                }
                onMouseEnter={this.handleMouseHover}
                onMouseLeave={this.handleMouseLeave}
                onClick={(e) => {
                    this.props.onClick();
                    e.stopPropagation();
                }}>
                <div
                    style={
                        {
                            width: 80,
                            height: 28,
                            borderRadius: 10,
                            paddingTop: 12,
                            backgroundColor: btnColor,
                            fontSize: 14,
                            color: "#FFFFFF"
                        }
                    }>
                    {btnName}
                </div>

                {/*<img*/}
                {/*    src={ iconSrc }*/}
                {/*    style={{*/}
                {/*        width:20,*/}
                {/*        height: 20,*/}
                {/*        position: 'absolute',*/}
                {/*        top: '50%',*/}
                {/*        left: '50%',*/}
                {/*        transform: 'translate(-50%, -50%)'*/}
                {/*    }}*/}
                {/*/>*/}
            </div>
        );
    }
}

export default ButtonControl;