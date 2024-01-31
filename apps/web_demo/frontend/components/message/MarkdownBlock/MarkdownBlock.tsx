
import MarkdownIt from "markdown-it";
// yarn add --dev @types/markdown-it
import mdHighlight from "markdown-it-highlightjs";
// @ts-ignore
import mdCodeCopy from "./markdownCopy";
import classes from './MarkdownBlock.module.css';
// import './markdown.css';
import { Stack, createTheme, Text, Box, useMantineTheme, useMantineColorScheme, rem, MantineFontSizesValues, Accordion } from "@mantine/core";
import { useState } from "react";


type MarkdownBlockProps = {
    content_type: string | undefined;
    content_tag: string | undefined;
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
      props.content_type == "main" || props.content_type == "system" ?
      <div
        style={{
          fontSize: rem(14),
          wordBreak: 'break-all'
        }}
        dangerouslySetInnerHTML={{ __html: htmlString() }}
      >
      </div> : 
      <Accordion style={{marginBottom: rem(7)}} variant="separated" defaultValue="Apples">
        <Accordion.Item key="Apples" value="Apples">
          <Accordion.Control style={{height: rem(32)}} icon="🧠">{props.content_tag}</Accordion.Control>
          <Accordion.Panel><div
            style={{
              fontSize: rem(14),
              wordBreak: 'break-all'
            }}
            dangerouslySetInnerHTML={{ __html: htmlString() }}
          >
          </div></Accordion.Panel>
      </Accordion.Item>
    </Accordion>
    );
  };