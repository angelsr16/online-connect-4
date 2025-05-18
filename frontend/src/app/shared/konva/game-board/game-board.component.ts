import { Component, EventEmitter, Input, Output } from '@angular/core';
import Konva from 'konva';
import { Grid } from '../../../core/models/Grid';
import { Game } from '../../../core/models/db/Game';
import { Circle } from 'konva/lib/shapes/Circle';

@Component({
  selector: 'app-game-board',
  imports: [],
  templateUrl: './game-board.component.html',
  styleUrl: './game-board.component.scss',
})
export class GameBoardComponent {
  @Input() gameData!: Game;
  @Input() player_id!: string;
  @Output() onGameClick: EventEmitter<number> = new EventEmitter();

  private stage!: Konva.Stage;
  private layer!: Konva.Layer;
  private cellSize: number = 0;
  private rows: number = 6;
  private cols: number = 7;

  hoverCircle!: Circle;

  constructor() {}

  ngAfterViewInit(): void {
    this.initKonva();
    window.addEventListener('resize', () => {
      this.stage.destroy();
      this.initKonva();
    });
  }

  private initKonva() {
    const container = document.getElementById('board-container');
    if (!container || !this.gameData) return;

    const rect = container.getBoundingClientRect();
    const containerWidth = rect.width;
    const containerHeight = rect.height;

    const cellWidth = (containerWidth / this.cols) * 0.75;
    const cellHeight = (containerHeight / this.rows) * 0.75;

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

    const grid = new Konva.Rect({
      x: 0,
      y: 0,
      width: this.cellSize * this.cols,
      height: this.cellSize * this.rows,
      fill: 'blue',
      stroke: '#000000',
      strokeWidth: 2,
      cornerRadius: 25,
    });
    this.layer.add(grid);

    this.stage.on('click', () => {
      const pos = this.stage.getPointerPosition();
      if (!pos) return;
      const column = Math.floor((pos.x / width) * this.cols);
      this.onGameClick.emit(column);
    });

    this.drawGrid();
  }

  updateGrid(gameData: Game) {
    this.gameData = gameData;
    this.drawGrid();
  }

  private drawGrid() {
    if (this.hoverCircle) {
      this.hoverCircle.remove();
    }

    for (
      let rowIndex = 0;
      rowIndex < this.gameData.game_state.length;
      rowIndex++
    ) {
      for (let colIndex = 0; colIndex < 7; colIndex++) {
        var color = '#fff';
        var cellValue = this.gameData.game_state[rowIndex][colIndex];
        switch (cellValue) {
          case 1:
            color = 'red';
            break;
          case 2:
            color = 'yellow';
            break;
        }

        this.drawCell(rowIndex, colIndex, color);
      }
    }

    if (!this.hoverCircle) {
      this.hoverCircle = new Konva.Circle({
        x: 0 * this.cellSize + this.cellSize / 2,
        y: 5 * this.cellSize + this.cellSize / 2,
        radius: this.cellSize / 2.5,
        fill:
          this.player_id === this.gameData.player_1.id ? '#ff6767' : '#f9ff9d',
      });

      this.stage.on('mousemove', () => {
        const pos = this.stage.getPointerPosition();
        if (!pos) return;
        const column = Math.floor(
          (pos.x / (this.cellSize * this.cols)) * this.cols
        );

        var rowPosCirclePreview = this.getCirclePreview(column);

        this.hoverCircle.position({
          x: column * this.cellSize + this.cellSize / 2,
          y: rowPosCirclePreview * this.cellSize + this.cellSize / 2,
        });

        this.layer.batchDraw();
      });
    }

    this.layer.add(this.hoverCircle);
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

  getCirclePreview(columnIndex: number): number {
    for (let row = this.gameData.game_state.length - 1; row >= 0; row--) {
      const cell = this.gameData.game_state[row][columnIndex];
      if (cell === 0) {
        return row;
      }
    }
    return -1;
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
