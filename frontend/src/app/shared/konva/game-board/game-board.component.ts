import { Component, EventEmitter, Input, Output } from '@angular/core';
import Konva from 'konva';
import { Grid } from '../../../core/models/Grid';

@Component({
  selector: 'app-game-board',
  imports: [],
  templateUrl: './game-board.component.html',
  styleUrl: './game-board.component.scss',
})
export class GameBoardComponent {
  @Input() gameGrid!: Grid;
  @Output() onGameClick: EventEmitter<number> = new EventEmitter();

  private stage!: Konva.Stage;
  private layer!: Konva.Layer;
  private cellSize: number = 0;
  private rows: number = 6;
  private cols: number = 7;

  constructor() {}

  ngAfterViewInit(): void {
    this.initKonva();
    window.addEventListener('resize', () => {
      this.stage.destroy();
      this.initKonva();
    });
  }

  // private initKonva() {
  //   const boardContainerRect = document
  //     .getElementById('board-container')
  //     ?.getBoundingClientRect();

  //   if (!boardContainerRect) return;

  //   const fullWidth: number = boardContainerRect.width;
  //   const fullHeight: number = boardContainerRect.height;

  //   this.cellSize = (fullHeight * 0.75) / 6;

  //   const width = this.cellSize * 7;
  //   const height = this.cellSize * 6;

  //   this.stage = new Konva.Stage({
  //     container: 'container',
  //     width,
  //     height,
  //   });

  //   this.stage.content.style.border = '1px solid black';

  //   this.layer = new Konva.Layer();
  //   this.stage.add(this.layer);

  //   const circle = new Konva.Circle({
  //     x: 0,
  //     y: 0,
  //     radius: this.cellSize / 2.5,
  //     fill: 'red',
  //   });

  //   this.layer.add(circle);
  //   this.layer.draw();

  //   this.stage.on('mousemove', () => {
  //     const pos = this.stage.getPointerPosition();
  //     if (!pos) return;

  //     circle.position({ x: pos.x, y: this.cellSize / 2 });
  //     this.layer.batchDraw();
  //   });

  //   this.stage.on('click', () => {
  //     const mousePos = this.stage.getPointerPosition();

  //     if (!mousePos) return;
  //     const xPos = Math.floor((mousePos.x / width) * 7);
  //     this.onGameClick.emit(xPos);
  //   });

  //   this.drawGrid();
  // }

  private initKonva() {
    const container = document.getElementById('board-container');
    if (!container) return;

    const rect = container.getBoundingClientRect();
    const containerWidth = rect.width;
    const containerHeight = rect.height;

    const cellWidth = (containerWidth / this.cols) * 0.85;
    const cellHeight = (containerHeight / this.rows) * 0.85;

    this.cellSize = Math.floor(Math.min(cellWidth, cellHeight));
    const width = this.cellSize * this.cols;
    const height = this.cellSize * this.rows;

    this.stage = new Konva.Stage({
      container: 'container',
      width,
      height,
    });

    this.layer = new Konva.Layer();
    this.stage.add(this.layer);

    const hoverCircle = new Konva.Circle({
      x: 0,
      y: 0,
      radius: this.cellSize / 2.5,
      fill: 'rgba(255,255,255,0.5)',
    });

    this.layer.add(hoverCircle);

    this.stage.on('mousemove', () => {
      const pos = this.stage.getPointerPosition();
      if (!pos) return;
      hoverCircle.position({ x: pos.x, y: this.cellSize / 2 });
      this.layer.batchDraw();
    });

    this.stage.on('click', () => {
      const pos = this.stage.getPointerPosition();
      if (!pos) return;
      const column = Math.floor((pos.x / width) * this.cols);
      this.onGameClick.emit(column);
    });

    this.drawGrid();
  }

  updateGrid(gameGrid: Grid) {
    this.gameGrid = gameGrid;
    this.drawGrid();
  }

  private drawGrid() {
    const grid = new Konva.Rect({
      x: 0,
      y: 0,
      width: this.cellSize * this.cols,
      height: this.cellSize * this.rows,
      fill: 'blue',
      stroke: '#000000',
      strokeWidth: 2,
    });
    this.layer.add(grid);

    this.gameGrid.forEach((row, rowIndex) => {
      row.forEach((col, colIndex) => {
        var color = '#fff';
        switch (col) {
          case 1:
            color = 'red';
            break;
          case 2:
            color = 'yellow';
            break;
        }

        this.drawCell(rowIndex, colIndex, color);
      });
    });

    this.layer.draw();
  }

  private drawCell(row: number, col: number, color: string) {
    const circle = new Konva.Circle({
      x: col * this.cellSize + this.cellSize / 2,
      y: row * this.cellSize + this.cellSize / 2,
      radius: this.cellSize / 2.5,
      fill: color,
      stroke: '#000000',
      strokeWidth: 2,
    });

    this.layer.add(circle);
  }

  onLeftClick() {
    console.log('Left arrow clicked');
    // You can add custom logic like navigating history or previewing moves
  }

  onRightClick() {
    console.log('Right arrow clicked');
    // Same as above, customize as needed
  }
}
