import { Text, SimpleGrid, Container, rem } from '@mantine/core';
import { IconTruck, IconCertificate, IconCoin, IconRobot, IconKeyboard } from '@tabler/icons-react';
import classes from './SelectCard.module.css';

interface FeatureProps extends React.ComponentPropsWithoutRef<'div'> {
  icon: React.FC<any>;
  title: string;
  description: string;
  caseId: string;
  callback: (value: string)=>void;
}

function Feature({ icon: Icon, title, description, caseId, callback, className, ...others }: FeatureProps) {
  return (
    <div style={{cursor: 'pointer'}} className={classes.feature} {...others} onClick={()=>callback(caseId)}>
      <div className={classes.overlay} />

      <div className={classes.content}>
        <Icon style={{ width: rem(38), height: rem(38) }} className={classes.icon} stroke={1.5} />
        <Text fw={700} fz="lg" mb="xs" mt={5} className={classes.title}>
          {title}
        </Text>
        <Text c="dimmed" fz="sm">
          {description}
        </Text>
      </div>
    </div>
  );
}

const mockdata = [
  {
    icon: IconRobot,
    title: '介绍数字员工',
    description:
      '什么是数字员工和数字部门？',
    caseId: "introduction"
  },
  {
    icon: IconCertificate,
    title: '合同审核',
    description:
      '如何让数字员工进行合同审核。',
    caseId: "contract_review"
  },
  {
    icon: IconKeyboard,
    title: '亲自体验',
    description:
      '快来和数字员工交流吧。',
    caseId: "/agent"
  },
];

type SelectCardProps = {
    callback: (value: string) => void;
  }

export function SelectCard(props: SelectCardProps) {
  const items = mockdata.map((item) => <Feature {...item} key={item.title} callback={props.callback} />);

  return (
    <SimpleGrid cols={{ base: 1, sm: 3 }} spacing={50}>
        {items}
      </SimpleGrid>
  );
}