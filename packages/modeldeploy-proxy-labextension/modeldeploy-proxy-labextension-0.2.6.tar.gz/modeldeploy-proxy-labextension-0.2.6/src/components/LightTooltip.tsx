import { Theme, withStyles } from '@material-ui/core/styles';
import { Tooltip } from '@material-ui/core';

export const LightTooltip = withStyles((theme: Theme) => ({
  tooltip: {
    backgroundColor: theme.palette.common.white,
    color: 'rgba(0, 0, 0, 0.87)',
    boxShadow: theme.shadows[1],
    fontSize: 'var(--jp-ui-font-size1)',
  },
}))(Tooltip);
