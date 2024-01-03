
import MarkdownIt from "markdown-it";
// yarn add --dev @types/markdown-it
import mdHighlight from "markdown-it-highlightjs";
// @ts-ignore
import mdCodeCopy from "./markdownCopy";
import classes from './MarkdownBlock.module.css';
// import './markdown.css';
import { Stack, createTheme, Text, Box, useMantineTheme, useMantineColorScheme, rem, MantineFontSizesValues } from "@mantine/core";
import { useState } from "react";


type MarkdownBlockProps = {
    content: string;
}

export default function MarkdownBlock(props: MarkdownBlockProps) {
    const htmlString = () => {
      let md = MarkdownIt({
        linkify: true,
        breaks: true,
      }).use(mdCodeCopy, {
        iconStyle: "", // Clear default icon style
        iconClass: classes.copyText, // Set a custom class for the icon element
        buttonStyle:
          "position: absolute; top: 7.5px; right: 6px; cursor: pointer; outline: none; border: none; background: none; color: #ffffff; background-color: #333;",
        buttonClass: "",
      });
  
    //   if (message.role === "assistant") {
      md = md.use(mdHighlight);
    //   }
  
      return md.render(props.content);
    };
  
    return (
      <div
        style={{fontSize: rem(14)}}
        // className={classes.message}
        dangerouslySetInnerHTML={{ __html: htmlString() }}
      >
      </div>
    );
  };